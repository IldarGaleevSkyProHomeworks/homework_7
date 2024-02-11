from rest_framework.routers import DefaultRouter

from app_users.apps import AppUsersConfig
from app_users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

app_name = AppUsersConfig.name

urlpatterns = [

]

urlpatterns += router.urls
