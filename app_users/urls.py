from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_users.apps import AppUsersConfig
from app_users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

app_name = AppUsersConfig.name

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
