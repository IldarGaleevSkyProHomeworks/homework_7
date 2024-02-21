from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_users"

    manager_group_name = 'manager'
    content_creator_group_name = 'creator'
