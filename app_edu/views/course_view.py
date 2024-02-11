from rest_framework import viewsets

from app_edu.models import Course
from app_edu.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
