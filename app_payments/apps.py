from django.apps import AppConfig


class AppPaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_payments"

    def ready(self):
        # https://docs.djangoproject.com/en/dev/topics/signals/#connecting-receiver-functions
        from app_payments.signals.handlers import init_signals
        # https://docs.djangoproject.com/en/dev/topics/signals/#preventing-duplicate-signals
        init_signals(self.name)
