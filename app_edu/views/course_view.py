from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app_edu.models import Course
from app_edu.pagination import AppEduPagination
from app_edu.serializers import CourseSerializer
from app_users.permissions import IsManager, IsOwner, IsContentCreator


class CourseViewSet(viewsets.ModelViewSet):
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
            case _:
                self.permission_classes = (IsAuthenticated, IsOwner | IsManager,)

        return [permission() for permission in self.permission_classes]
