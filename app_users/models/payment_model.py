from django.db import models

from .user_model import User

from app_edu.models import Lesson, Course


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

    lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Урок'
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Курс'
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

    @property
    def purchased_product(self):
        if self.lesson:
            return self.lesson

        if self.course:
            return self.course

        return None

    def __str__(self):
        product = self.purchased_product
        if product:
            product_name = f'{product._meta.verbose_name} "{product.name}"'
        else:
            product_name = 'Unknown'

        return f'{self.user}: {product_name} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)
