from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Post
from django.utils import timezone
from datetime import timedelta
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(day_of_week='*/1')),
    name="task_deactivate_old_post",
    ignore_result=True
)
def task_deactivate_old_post():
    posts = Post.objects.all()
    for post in posts:
        if post.is_active:
            if (post.updated + timezone.timedelta(days=30)) <= timezone.now():
                post.is_active = False
                post.save()
                logger.info('post:{0} deactivated'.format(post.id))
