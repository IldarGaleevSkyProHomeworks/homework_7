from celery import shared_task
from app_payments.services import stripe
import logging

logger = logging.getLogger(__name__)


@shared_task
def create_product_course_task(course_id: int):
    stripe.create_product_course(course_id)


@shared_task
def delete_product_course_task(stripe_product_id: str):
    stripe.delete_product_course(stripe_product_id)


@shared_task
def update_product_course_task(course_id: int, updates: dict):
    stripe.update_product_course(course_id, updates)


@shared_task
def create_invoice_for_user_task(user_id: int, course_id: int, base_url: str):
    stripe.create_invoice_for_user(user_id, course_id, base_url)
