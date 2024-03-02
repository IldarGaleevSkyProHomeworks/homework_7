from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_edu.models import Course, Subscription
from app_edu.pagination import AppEduPagination
from app_edu.serializers import CourseSerializer, SubscriptionSerializer, SubscriptionStatusSerializer, \
    SubscriptionDeleteStatusSerializer
from app_payments.models import Payment
from app_payments.serializers import PaymentStatusSerializer
from app_payments.services.stripe import create_invoice_for_user, get_or_create_payment
from app_users.permissions import IsManager, IsOwner, IsContentCreator
from utils.serializers import StatusSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
        create:
        Создание курса.

        retrieve:
        Информация о курсе.

        list:
        Возвращает список курсов.

        update:
        Править информацию о курсе.

        partial_update:
        Править часть полей курса.

        delete:
        Удалить курс.

        subscribe:
        Подписаться на курс

        unsubscribe:
        Отписаться от курса

    """

    serializer_class = CourseSerializer
    pagination_class = AppEduPagination

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.action != 'list' or self.request.user.is_manager:
            return queryset

        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        match self.action:
            case 'create':
                self.permission_classes = (IsAuthenticated, IsContentCreator,)
            case 'destroy':
                self.permission_classes = (IsAuthenticated, IsOwner,)
            case 'subscribe' | 'unsubscribe' | 'buy':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsOwner | IsManager,)

        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SubscriptionStatusSerializer(),
            status.HTTP_201_CREATED: SubscriptionStatusSerializer(),
        },
        request_body=no_body
    )
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk: int = None):
        course = get_object_or_404(Course, pk=pk)
        subs, is_created = Subscription.objects.get_or_create(
            user=self.request.user, course=course
        )

        response = {
            'data': SubscriptionSerializer(subs).data,
        }
        if is_created:
            response['detail'] = 'Курс сохранен в подписки'
            status_code = status.HTTP_201_CREATED
        else:
            response['detail'] = 'Вы уже подписаны на данный курс'
            status_code = status.HTTP_200_OK

        return Response(StatusSerializer(response).data, status_code)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SubscriptionDeleteStatusSerializer()
        }
    )
    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk: int = None):
        course = get_object_or_404(Course, pk=pk)
        deleted, _ = course.subscriptions.filter(user=request.user).delete()
        response = {
            'deleted': deleted,
            'detail': f'Подписка на курс "{course.name}" удалена' if deleted > 0 else 'Нет подписки'
        }

        return Response(
            SubscriptionDeleteStatusSerializer(response).data,
            status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Купить курс",
        responses={
            status.HTTP_102_PROCESSING: StatusSerializer(),
            status.HTTP_201_CREATED: None
        },
        request_body=no_body
    )
    @action(detail=True, methods=['post'])
    def buy(self, request, pk: int = None):
        curr_user = request.user
        course = get_object_or_404(Course, pk=pk)
        payment = get_or_create_payment(user_id=curr_user.pk, course_id=course.pk)

        response = {
            'status': payment.payment_status,
            'data': payment
        }

        if payment.payment_status == Payment.PaymentStatus.paid:
            response['detail'] = 'Вы уже оплатили этот курс.'
        elif payment.payment_status == Payment.PaymentStatus.waited and payment.payment_link:
            response['detail'] = 'Счет уже выставлен и ждет оплаты.'
        else:
            create_invoice_for_user(user_id=curr_user.pk, course_id=course.pk, base_url=request.get_host())
            response['detail'] = ('Платеж создан. Ссылка на оплату доступна в платежах. '
                                  'Если ссылка отстутствует повторите запрос через некоторое время.')

        return Response(
            data=PaymentStatusSerializer(response).data,
            status=status.HTTP_200_OK
        )
