from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_payments.views import PaymentsViewSet
from app_users.apps import AppUsersConfig

router = DefaultRouter()
router.register('', PaymentsViewSet, basename='payments')

app_name = AppUsersConfig.name

urlpatterns = [
    path('', include(router.urls)),
]
