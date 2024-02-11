from django.urls import path
from rest_framework.routers import DefaultRouter

from app_edu.apps import AppEduConfig
from app_edu.views import (CourseViewSet, LessonListViewSet, LessonRetrieveView, LessonCreateView,
                           LessonUpdateView, LessonDeleteView)

app_name = AppEduConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListViewSet.as_view(), name='lesson_list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(http_method_names=['get']), name='lesson_detail'),
    path('lessons/<int:pk>/change/', LessonUpdateView.as_view(http_method_names=['put']), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(http_method_names=['delete']), name='lesson_delete'),
]

urlpatterns += router.urls
