from rest_framework import serializers

from app_edu.models import Lesson
from app_edu.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        curr_user = self.context['request'].user
        new_lesson = super().create(validated_data)
        new_lesson.owner = curr_user
        new_lesson.save()
        return new_lesson

    class Meta:
        model = Lesson
        exclude = ('courses',)
        read_only_fields = ('owner',)
        validators = [VideoUrlValidator('video_url')]
        swagger_schema_fields = {
            "description": "Информация об уроке"
        }
