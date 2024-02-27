import re

from rest_framework import serializers


class VideoUrlValidator:
    regex = r"https:\/\/(www\.)?((youtube\.com\/watch\?v=)|(youtu\.be\/))[\w\d]+"

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get(self.field)

        if video_url is None:
            return

        if not re.match(self.regex, video_url, re.IGNORECASE):
            raise serializers.ValidationError({
                self.field: 'Неверный формат url. Используйте только youtube-ссылки'
            })
