import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toturial2.settings')
application = get_wsgi_application()

from django_q.models import Schedule
from myapp.cron.func import check_and_update_task_status
def schedule_task():
    schedule, created = Schedule.objects.get_or_create(
        name='check_task_pending',
        func='myapp.cron.func.check_and_update_task_status',  # Replace 'myapp' with your app name
        schedule_type=Schedule.MINUTES,
        minutes=5,
    )

    if created:
        print("Task scheduled successfully")
    else:
        print("Task schedule already exists")

# schedule_task()
check_and_update_task_status()