from rest_framework import serializers

from app_edu import validators
from app_edu.models import Course, Lesson
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
