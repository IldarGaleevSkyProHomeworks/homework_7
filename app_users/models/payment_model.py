from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .user_model import User

from app_edu.models import Lesson, Course


class PurchasedProduct(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Урок',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Курс',
    )

    @property
    def product_instance(self):
        if self.lesson:
            return self.lesson

        if self.course:
            return self.course

        return None

    def __str__(self):
        instance = self.product_instance
        return f'{instance._meta.verbose_name} - {instance.name}' if instance else 'Unknown'

    class Meta:
        # TODO: add custom clean. NONE is not unique
        unique_together = ('lesson', 'course')
        verbose_name = 'Продукт для продажи'
        verbose_name_plural = 'Продукты для продажи'


class Payment(models.Model):
    class PaymentMethodEnum(models.IntegerChoices):
        unknown = 0, 'Неизвестно'
        cash = 1, 'Наличные'
        transfer = 2, 'Перевод на счет'

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    purchased_product = models.ForeignKey(
        PurchasedProduct,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Купленый продукт',
    )

    payment_date = models.DateField(
        auto_now=True,
        verbose_name='Дата оплаты'
    )

    payment_amount = models.DecimalField(
        default=0.0,
        decimal_places=3,
        max_digits=9,
        verbose_name='Сумма оплаты'
    )

    payment_method = models.PositiveSmallIntegerField(
        choices=PaymentMethodEnum.choices,
        default=PaymentMethodEnum.unknown,
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f'{self.user}: {self.purchased_product} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)
