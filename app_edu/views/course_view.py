from rest_framework import viewsets

from app_edu.models import Course
from app_edu.serializers import CourseSerializer
from app_users.apps import AppUsersConfig
from app_users.permissions import IsManager, IsOwner, IsContentCreator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

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
