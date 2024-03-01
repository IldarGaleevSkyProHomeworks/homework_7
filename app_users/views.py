from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from app_users.models import User
from app_users.pagination import AppUserPagination
from app_users.permissions import IsAnonCreate
from app_users.serializers import UserSerializer, UserSafeSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
            create:
            Регистрация нового пользователя.

            retrieve:
            Информация о пользователе.

            list:
            Возвращает список пользователей.

            update:
            Править информацию о пользователе.

            partial_update:
            Править часть информации о пользователе.

        """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAnonCreate | IsAuthenticated,)
    pagination_class = AppUserPagination

    def get_serializer_class(self):
        is_swagger = getattr(self, 'swagger_fake_view', False)

        if self.action == 'list':
            return UserSafeSerializer
        if is_swagger or self.action == 'create' or self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserSafeSerializer
