from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from app_users.models import User, Payment
from app_users.pagination import AppUserPagination
from app_users.serializers import UserSerializer, PaymentSerializer, UserSafeSerializer
from app_users.permissions import IsAnonCreate


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAnonCreate | IsAuthenticated,)
    pagination_class = AppUserPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSafeSerializer
        if self.action == 'create' or self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserSafeSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('payment_method', )
    ordering_fields = ('payment_date',)
    pagination_class = AppUserPagination
