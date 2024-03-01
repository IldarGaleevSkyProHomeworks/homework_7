from rest_framework import serializers

from app_edu.serializers import SubscriptionSerializer
from app_payments.serializers import PaymentSerializer
from app_users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, write_only=True)

    subscriptions = SubscriptionSerializer(
        source='subscriptions.all',
        many=True,
        read_only=True,
        remove_fields=('user',)
    )
    payments = PaymentSerializer(
        source='payment_set.all',
        many=True,
        read_only=True,
        remove_fields=('user',)
    )

    def get_subscriptions(self, obj: User):
        return

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        exclude = ('is_superuser',)
        swagger_schema_fields = {
            "description": "Полная информация о пользователе"
        }


class UserSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone',)
        read_only_fields = ('email', 'phone',)
        swagger_schema_fields = {
            "title": "UserPublic",
            "description": "Публичная информация о пользователе"
        }
