from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=False, read_only=True, default='Ok')
    data = serializers.DictField(required=False, read_only=True, default=None)
    detail = serializers.CharField(required=False, read_only=True, default=None)
