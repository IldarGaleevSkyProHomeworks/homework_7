from django.db import models

from app_edu.models import Course


class StripeProductCourse(models.Model):
    stripe_product_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='идентификатор товара в Stripe'
    )

    stripe_default_price_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='идентификатор ценника в Stripe'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
