import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from app_edu.models import Course

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': settings.CELERY_TASK_RETRY_COUNT}
)
def notify_subscribed_users_task(self, course_id: int):
    course: Course = Course.objects.filter(pk=course_id).first()

    if course is None:
        logger.warning(f'Unknown course id: {course_id}')
        return

    for subscriber in [subscription.user for subscription in course.subscriptions.all()]:
        ctx = {
            'object': course,
        }

        html_body = render_to_string('email/course_changed_notifying.html', context=ctx)

        msg = EmailMultiAlternatives(
            subject=f'Курс "{course.name}" обновился',
            to=[subscriber.email]
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()
