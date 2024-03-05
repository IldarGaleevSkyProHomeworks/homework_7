from django.db.models import signals as model_signals

from app_edu import signals as app_edu_signals
from app_edu.models import Course
from app_payments import tasks


def handler_create_course(sender, instance: Course, **kwargs):
    tasks.create_product_course_task.delay(instance.pk)


def handler_update_course(sender, instance: Course, updates, **kwargs):
    tasks.update_product_course_task.delay(instance.pk, updates)


def handler_delete_course(sender, instance: Course, **kwargs):
    stripe_products = instance.stripeproductcourse_set.all()
    if stripe_products.exists():
        tasks.delete_product_course_task.delay(stripe_products.first().stripe_product_id)


def init_signals(dispatch_uid):
    app_edu_signals.course_post_create.connect(
        handler_create_course,
        sender=Course,
        dispatch_uid=dispatch_uid
    )

    app_edu_signals.course_post_update.connect(
        handler_update_course,
        sender=Course,
        dispatch_uid=dispatch_uid
    )

    model_signals.pre_delete.connect(
        handler_delete_course,
        sender=Course,
        dispatch_uid=dispatch_uid
    )
