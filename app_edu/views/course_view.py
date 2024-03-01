from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_edu.models import Course, Subscription
from app_edu.pagination import AppEduPagination
from app_edu.serializers import CourseSerializer, SubscriptionSerializer
from app_users.permissions import IsManager, IsOwner, IsContentCreator


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
            case 'subscribe' | 'unsubscribe':
                self.permission_classes = (IsAuthenticated,)
            case _:
                self.permission_classes = (IsAuthenticated, IsOwner | IsManager,)

        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk: int = None):
        course = get_object_or_404(Course, pk=pk)
        subs, is_created = Subscription.objects.get_or_create(
            user=self.request.user, course=course
        )

        response = {
            'results': SubscriptionSerializer(subs).data,
        }
        if is_created:
            response['detail'] = 'Курс сохранен в подписки'
            status_code = status.HTTP_201_CREATED
        else:
            response['detail'] = 'Вы уже подписаны на данный курс'
            status_code = status.HTTP_200_OK

        return Response(response, status_code)

    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk: int = None):
        course = get_object_or_404(Course, pk=pk)
        deleted, _ = course.subscriptions.filter(user=request.user).delete()
        response = {
            'deleted': deleted,
            'detail': f'Подписка на курс "{course.name}" удалена' if deleted > 0 else 'Нет подписки'
        }

        return Response(
            response,
            status.HTTP_200_OK
        )
