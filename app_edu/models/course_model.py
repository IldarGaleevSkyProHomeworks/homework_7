from django.db import models

from app_users.models import User
from utils.hash_storage import HashStorage, course_preview_images


class Course(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название'
    )

    description = models.TextField(
        max_length=1024,
        verbose_name='Описание'
    )

    preview = models.ImageField(
        upload_to=course_preview_images,
        storage=HashStorage(),
        null=True,
        blank=True,
        verbose_name='Превью',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        related_name='courses',
        verbose_name='владелец'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
