from django.contrib.auth.views import LogoutView, LoginView
from rest_framework.routers import DefaultRouter

from app_users.apps import AppUsersConfig
from django.urls import path
from app_users.views import UserViewSet, PaymentsViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('payments', PaymentsViewSet, basename='payments')

app_name = AppUsersConfig.name

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
