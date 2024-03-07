from celery import shared_task
from django.conf import settings

from app_payments.services import stripe


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': settings.CELERY_TASK_RETRY_COUNT}
)
def create_product_course_task(self, course_id: int):
    stripe.create_product_course(course_id)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': settings.CELERY_TASK_RETRY_COUNT}
)
def delete_product_course_task(stripe_product_id: str):
    stripe.delete_product_course(stripe_product_id)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': settings.CELERY_TASK_RETRY_COUNT}
)
def update_product_course_task(self, course_id: int, updates: dict):
    stripe.update_product_course(course_id, updates)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': settings.CELERY_TASK_RETRY_COUNT}
)
def create_invoice_for_user_task(self, user_id: int, course_id: int, base_url: str):
    stripe.create_invoice_for_user(user_id, course_id, base_url)


@shared_task
def stripe_poll_status():
    stripe.stripe_poll_status()
