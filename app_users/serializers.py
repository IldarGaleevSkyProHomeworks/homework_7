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
    payments = PaymentSerializer(
        source='payment_set.all',
        many=True,
        remove_fields=('user',)
    )

    class Meta:
        model = User
        exclude = ('password', 'is_superuser')
