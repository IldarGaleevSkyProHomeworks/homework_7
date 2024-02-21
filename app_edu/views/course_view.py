from rest_framework import viewsets

from app_edu.models import Course
from app_edu.serializers import CourseSerializer
from app_users.permissions import IsManager, IsOwner, IsContentCreator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        match self.action:

            case 'create':
                self.permission_classes = (IsContentCreator,)
            case 'update':
                self.permission_classes = (IsOwner | IsManager,)
            case 'destroy':
                self.permission_classes = (IsOwner,)
            case 'retrieve':
                self.permission_classes = (IsOwner | IsManager,)
            case 'list':
                self.permission_classes = (IsAuthenticated,)
                # self.permission_classes = (IsOwner | IsManager,)
            case _:
                self.permission_classes = ()

        return [permission() for permission in self.permission_classes]
