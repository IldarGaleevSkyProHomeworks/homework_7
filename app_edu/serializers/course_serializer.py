from rest_framework import serializers

from app_edu.models import Course
from app_edu.signals import course_post_create, course_post_update
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
        course_post_create.send(Course, instance=new_course)
        return new_course

    def update(self, instance, validated_data):
        updated_course = super().update(instance, validated_data)
        course_post_update.send(Course, instance=updated_course, updates=validated_data)
        return updated_course

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)
        swagger_schema_fields = {
            "description": "Информация о курсе"
        }
