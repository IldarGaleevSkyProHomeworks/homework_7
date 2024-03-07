from django.apps import AppConfig


class AppEduConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_edu"
    verbose_name = 'Образовательная платформа'

    def ready(self):
        # https://docs.djangoproject.com/en/dev/topics/signals/#connecting-receiver-functions
        from app_edu.signals.handlers import init_signals
        # https://docs.djangoproject.com/en/dev/topics/signals/#preventing-duplicate-signals
        init_signals(self.name)
