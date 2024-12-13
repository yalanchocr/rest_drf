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
        hours=20,
    )

    if created:
        print("Task scheduled successfully")
    else:
        print("Task schedule already exists")

from myapp.models import Task
from datetime import datetime, timedelta
from django_q.models import Task as QTask

def update_task_status():
    # Calculate the threshold for tasks being 12 hours old
    threshold = datetime.now() - timedelta(hours=12)

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

# schedule_task()
# check_and_update_task_status()
# from django_q.tasks import fetch
# from django_q.models import OrmQ
# from django_q.models import Task as QTask

# Assuming you have the task ID
# q_task_id = 'a9e60ca4668b4138a943eb568b3489b6'
# try:
#     # Check the task status in Django-Q
#     q_task = QTask.objects.filter(id=q_task_id).first()
#
#     if q_task:
#         if q_task.success:
#             # Task is complete
#             print("completed")
#         elif not q_task.success and q_task.stopped:
#             # Task failed
#             print("failed")
#         # Save the updated status
#         # task.save()
#     else:
#         # If the task is not found in Django-Q
#         print("unknown")
#         # task.save()
# except Exception as e:
#     # Handle any exceptions (logging, etc.)
#     print(f"Error updating task {q_task_id}: {e}")

# task = fetch(task_id)

# if task:
#     # Check task status
#     if task.success:
#         print("Task completed successfully")
#         print("Result:", task.result)
#     elif task.failed:
#         print("Task failed")
#         print("Error:", task.exc_info)
#     else:
#         print("Task is still in progress")
# else:
#     print("Task not found")