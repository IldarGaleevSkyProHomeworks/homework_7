from django.db import models

from app_payments.models import Payment


class StripeSession(models.Model):
    stripe_session_id = models.CharField(
        max_length=150,
        verbose_name='идентификатор сессии Stripe'
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        verbose_name='связанный платеж'
    )
