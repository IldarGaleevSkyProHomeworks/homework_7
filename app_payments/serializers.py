from rest_framework import serializers

from app_payments.models import Payment
from utils.serializers import StatusSerializer


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
        swagger_schema_fields = {
            "description": "Информация о платежах"
        }


class PaymentStatusSerializer(StatusSerializer):
    data = PaymentSerializer()
