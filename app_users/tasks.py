from django.conf import settings
from django.utils.timezone import localdate

from celery import shared_task

from app_users.models import User


@shared_task
def disable_inactive_users_task():
    deadline_date = localdate() - settings.INACTIVE_USERS_INTERVAL

    inactive_users = User.objects.filter(last_login__lte=deadline_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
