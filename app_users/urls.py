from rest_framework.routers import DefaultRouter

from app_users.apps import AppUsersConfig
from app_users.views import UserViewSet, PaymentsViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('payments', PaymentsViewSet, basename='payments')

app_name = AppUsersConfig.name

urlpatterns = [

]

urlpatterns += router.urls
