from django.db import models

from .course_model import Course
from app_users.models import User


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Владелец'
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']
        unique_together = ['user', 'course', ]

    def __str__(self):
        user = self.user
        course = self.course
        return f'{user} подписан на {course}'
