from django.db import models

from app_users.models import User

from app_edu.models import Lesson, Course


class Payment(models.Model):
    class PaymentStatus(models.IntegerChoices):
        unknown = 0, 'Неизвестно'
        waited = 1, 'Ожидание оплаты'
        paid = 2, 'Оплачено'
        cancelled = 3, 'Отменено'
        expired = 4, 'Время ожидания истекло'

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
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

    payment_method = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Способ оплаты'
    )

    payment_link = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='ссылка на оплату'
    )

    payment_link_expires_at = models.DateTimeField(
        auto_now=False,
        null=True,
        blank=True,
        verbose_name='время окончания действия ссылки',
    )

    payment_status = models.SmallIntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.unknown,
        verbose_name='статус платежа'
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
