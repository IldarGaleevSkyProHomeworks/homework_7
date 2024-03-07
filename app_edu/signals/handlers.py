from app_edu import tasks
from app_edu.models import Course

from app_edu import signals as app_edu_signals


def handler_update_course(sender, instance: Course, **kwargs):
    tasks.notify_subscribed_users_task.delay(instance.pk)


def init_signals(dispatch_uid):
    app_edu_signals.course_post_update.connect(
        handler_update_course,
        sender=Course,
        dispatch_uid=dispatch_uid
    )
