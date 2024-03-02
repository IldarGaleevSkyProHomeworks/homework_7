import logging

import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app_payments.models import Payment
from app_payments.pagination import AppPaymentPagination
from app_payments.serializers import PaymentSerializer, PaymentStatusSerializer
from app_payments.services.stripe import stripe_update_session_status

logger = logging.getLogger(__name__)


class PaymentsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
            retrieve:
            Информация о платеже.

            list:
            Возвращает список платежей.
        """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('payment_method',)
    ordering_fields = ('payment_date',)
    pagination_class = AppPaymentPagination

    def get_queryset(self):
        queryset = Payment.objects.all()
        if self.action != 'list' or self.request.user.is_manager:
            return queryset

        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        match self.action:
            case 'success':
                self.permission_classes = [AllowAny]
            case _:
                self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        operation_description="Эндпоинт для редиректа после оплаты",
        responses={
            status.HTTP_200_OK: PaymentStatusSerializer()
        })
    @action(detail=True, methods=['get'])
    def success(self, request, pk: int = None):
        payment = get_object_or_404(Payment, pk=pk)
        response = {
            "data": payment,
            "detail": "Оплачено"
        }
        return Response(
            data=PaymentStatusSerializer(response).data,
            status=status.HTTP_200_OK
        )

    # @swagger_auto_schema(responses={status.HTTP_200_OK: 'ok'})
    # @action(detail=True, methods=['get'])
    # def cancel(self, request, pk: int = None):
    #     return Response(StatusSerializer({"detail": "Платеж отменен"}).data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """
    Вебхук для Stripe
    """

    event = None
    payload = request.body
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    if sig_header is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        logger.error(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        logger.error(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        data = event['data']['object']
        stripe_update_session_status(
            stripe_session_id=data['id'],
            new_status=data['payment_status'],
            new_amount=int(data['amount_total']) / 100.00,
            new_payment_method=data['payment_method_types'][0],
        )
    else:
        logger.warning(f'Unhandled event type {event["type"]}')

    return Response({'success': True})
