from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from utils.hash_storage import user_avatar_images, HashStorage


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=24,
        null=True,
        blank=True,
        verbose_name='Телефон',
    )

    city_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Город'
    )

    avatar = models.ImageField(
        upload_to=user_avatar_images,
        storage=HashStorage(),
        null=True,
        verbose_name='Аватар',
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def short_str(self):
        return f'{self.first_name}' if self.first_name else self.email

    def __str__(self):
        return f'{self.first_name} ({self.email})' if self.first_name else self.email

    class Meta:
        permissions = [
        ]
