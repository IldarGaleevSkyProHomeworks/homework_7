from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter

from app_payments.models import Payment
from app_payments.pagination import AppPaymentPagination
from app_payments.serializers import PaymentSerializer


class PaymentsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
            create:
            Создание платежа.

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
