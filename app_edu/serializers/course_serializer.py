from rest_framework import serializers

from app_edu.models import Course
from .lesson_serializer import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def create(self, validated_data):
        curr_user = self.context['request'].user
        new_course = super().create(validated_data)
        new_course.owner = curr_user
        new_course.save()
        return new_course

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)
