import functools
import logging as py_log
from datetime import datetime

import pytz
import stripe as stripe_api
from django.conf import settings
from django.urls import reverse_lazy

import app_edu.models as edu_models
from app_payments.models import StripeProductCourse, Payment
from app_payments.models.stripe_session_model import StripeSession
from app_users.models import User

stripe_api.api_key = settings.STRIPE_API_KEY

logging = py_log.getLogger(__name__)


def _create_product_course(course_id):
    cached_product = StripeProductCourse.objects.filter(course_id=course_id)
    if cached_product.exists():
        return cached_product[0]

    course = edu_models.Course.objects.get(pk=course_id)

    product_info = stripe_api.Product.search(
        query=f'active:"true" AND metadata["course_id"]:"{course.pk}"'
    ).data

    if product_info:
        product_info = product_info[0]
    else:
        product_info = stripe_api.Product.create(
            name=course.name,
            description=course.description,
            default_price_data={
                'currency': 'RUB',  # TODO: may be parameterized...
                'unit_amount': int(course.price * 100),
                'tax_behavior': 'inclusive',
            },
            metadata={
                'course_id': course.pk
            }
        )

    stripe_product = StripeProductCourse.objects.create(
        stripe_product_id=product_info.id,
        stripe_default_price_id=str(product_info.default_price),
        course=course
    )
    stripe_product.save()
    return stripe_product


def get_or_create_stripe_product(course_id) -> StripeProductCourse:
    stripe_product = StripeProductCourse.objects.filter(course_id=course_id)
    if stripe_product.exists():
        return stripe_product.first()
    return _create_product_course(course_id)


def create_product_course(course_id):
    _create_product_course(course_id)


def delete_product_course(stripe_product_id):
    stripe_api.Product.modify(
        stripe_product_id,
        active=False
    )


def update_product_course(course_id, updates):
    updated_course = StripeProductCourse.objects.filter(course_id=course_id).first()
    if updated_course is None:
        _create_product_course(course_id)
        return
    changes = {}

    if new_name := updates.get('name'):
        changes['name'] = new_name

    if new_description := updates.get('description'):
        changes['description'] = new_description

    if new_price := updates.get('price'):
        new_price = stripe_api.Price.create(
            product=updated_course.stripe_product_id,
            currency='RUB',  # TODO: may be parameterized...
            unit_amount=int(float(new_price) * 100),
            tax_behavior='inclusive',
        )
        changes['default_price'] = new_price.id
        updated_course.stripe_default_price_id = new_price.id
        updated_course.save()

    stripe_api.Product.modify(
        updated_course.stripe_product_id,
        **changes
    )


def get_or_create_payment(user_id, course_id):
    payment, _ = Payment.objects.get_or_create(user_id=user_id, course_id=course_id)
    return payment


def create_invoice_for_user(user_id, course_id, base_url):
    payment = get_or_create_payment(user_id, course_id)

    if payment.PaymentStatus != Payment.PaymentStatus.paid:
        product = get_or_create_stripe_product(course_id)

        # TODO: scheme hardcoded!
        success_url = f'{settings.APPLICATION_SCHEME}://{base_url}{reverse_lazy("app_payments:payments-success", kwargs={"pk": payment.pk})}'
        # cancel_url = f'http://{base_url}{reverse_lazy("app_payments:payments-cancel", kwargs={"pk": payment.pk})}'

        session_info = stripe_api.checkout.Session.create(
            mode='payment',
            customer_email=payment.user.email,
            line_items=[
                {
                    "quantity": 1,
                    "price": product.stripe_default_price_id
                }
            ],

            success_url=success_url,
            # cancel_url=cancel_url,
        )

        payment.payment_link = session_info.url
        payment.payment_link_expires_at = datetime.fromtimestamp(session_info.expires_at,
                                                                 tz=pytz.timezone(settings.TIME_ZONE))
        payment.payment_status = Payment.PaymentStatus.waited
        payment.payment_amount = product.course.price
        payment.save()

        StripeSession.objects.create(
            stripe_session_id=session_info.id,
            payment=payment
        ).save()


def stripe_poll_status():
    sessions = StripeSession.objects.all()
    for session in sessions:
        try:
            stripe_session = stripe_api.checkout.Session.retrieve(session.stripe_session_id)
            stripe_update_session_status(
                stripe_session=session,
                new_amount=stripe_session.amount_total / 100.0,
                new_payment_method=stripe_session.payment_method_types[0],
                new_status=stripe_session.payment_status,
            )
        except Exception as e:
            logging.error(e)


def stripe_update_session_status(
        stripe_session: StripeSession = None,
        stripe_session_id: str = None,
        new_status: str = None,
        new_amount: float = None,
        new_payment_method: str = None
):
    if stripe_session is None and stripe_session_id is None:
        raise Exception('Bad arguments. Required to specify stripe_session or stripe_session_id')

    stripe_session = stripe_session or StripeSession.objects.filter(stripe_session_id=stripe_session_id).first()
    if not stripe_session:
        logging.warning(f'Unknown session id "{stripe_session_id}" received')
        return

    if new_status == 'paid':
        stripe_session.payment.payment_amount = new_amount
        stripe_session.payment.payment_method = new_payment_method
        stripe_session.payment.payment_status = Payment.PaymentStatus.paid
        stripe_session.payment.payment_link = None
        stripe_session.delete()
    elif new_status == 'expired':
        stripe_session.payment.payment_status = Payment.PaymentStatus.expired
        stripe_session.payment.payment_link = None
        stripe_session.delete()
    stripe_session.payment.save()
