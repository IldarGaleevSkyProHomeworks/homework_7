from rest_framework import serializers

from app_users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, write_only=True)
    payments = PaymentSerializer(
        source='payment_set.all',
        many=True,
        read_only=True,
        remove_fields=('user',)
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        exclude = ('is_superuser',)


class UserSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone',)
        read_only_fields = ('email', 'phone',)
