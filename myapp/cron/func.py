from django_q.tasks import async_task
from myapp.models import Task  # Replace with your actual Task model import
from django.db import transaction
from datetime import datetime, timedelta

from myapp.models import Task
from datetime import datetime, timedelta
from django_q.models import Task as QTask
from django_q.models import Schedule


def update_task_status():
    # Calculate the threshold for tasks being 12 hours old
    threshold = datetime.utcnow() - timedelta(hours=12)

    # Filter tasks based on status and creation time
    pending_tasks = Task.objects.filter(
        status=Task.PENDING,
        created_at__lt=threshold,  # Filter tasks created before the threshold
    )
    for task in pending_tasks:
        try:
            if task.q_task_id is None:
                task.set_status_failed("problem in create a async task for doing")
                # Optionally, you can log the update
                print(f"Updated task: {task.id}")
            else:
                # Check the task status in Django-Q
                q_task = QTask.objects.filter(id=task.q_task_id).first()

                if q_task:
                    if q_task.success:
                        task.set_status_successful(q_task.result)
                    elif not q_task.success and q_task.stopped:
                        # Task failed
                        task.set_status_failed(q_task.result)

                else:
                    # If the task is not found in Django-Q
                    task.set_status_failed("problem in create a async task for doing")
        except Exception as e:
            # Handle any exceptions (logging, etc.)
            print(f"Error updating task {task.q_task_id}: {e}")


def check_and_update_task_status():
    with transaction.atomic():
        update_task_status()



def schedule_task():
    schedule, created = Schedule.objects.get_or_create(
        name='check_task_pending',
        func='myapp.cron.func.check_and_update_task_status',  # Replace 'myapp' with your app name
        schedule_type=Schedule.DAILY,  # Schedule based on hours
    )

    if created:
        print("Task scheduled successfully")
    else:
        print("Task schedule already exists")
