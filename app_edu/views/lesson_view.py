from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_edu.models import Lesson
from app_edu.pagination import AppEduPagination
from app_edu.serializers import LessonSerializer
from app_users.apps import AppUsersConfig
from app_users.permissions import IsOwner, IsManager, IsContentCreator


class LessonListViewSet(generics.ListAPIView):
    """
    Список уроков
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AppEduPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name=AppUsersConfig.manager_group_name).exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Информация об уроке
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsManager,)


class LessonCreateView(generics.CreateAPIView):
    """
    Создать урок
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsContentCreator,)


class LessonDeleteView(generics.DestroyAPIView):
    """
    Удалить урок
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner,)


class LessonUpdateView(generics.UpdateAPIView):
    """
    Обновить информацию об уроке
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsManager,)
