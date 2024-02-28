from rest_framework import viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_edu.models import Course, Subscription
from app_edu.pagination import AppEduPagination
from app_edu.serializers import CourseSerializer, SubscriptionSerializer
from app_users.apps import AppUsersConfig
from app_users.permissions import IsManager, IsOwner, IsContentCreator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = AppEduPagination

    def get_queryset(self):
        if self.action != 'list' or self.request.user.groups.filter(name=AppUsersConfig.manager_group_name).exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        match self.action:
            case 'create':
                self.permission_classes = (IsContentCreator,)
            case 'destroy':
                self.permission_classes = (IsOwner,)
            case _:
                self.permission_classes = (IsOwner | IsManager,)

        return [permission() for permission in self.permission_classes]


class SubscribeUnsubscribeAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])

        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.name} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.name} удален из подписок',
        }
        return Response(response, status.HTTP_204_NO_CONTENT)
