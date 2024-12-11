from django_q.tasks import async_task
from myapp.models import Task  # Replace with your actual Task model import
from django.db import transaction


def check_and_update_task_status():
    with transaction.atomic():
        # Get all tasks that are not in the desired status
        tasks = Task.objects.filter(status=Task.PENDING)

        # Update the status of these tasks
        for task in tasks:
            if task.q_task_id is None:
                task.set_status_failed("problem in create a async task for doing")
                # Optionally, you can log the update
                print(f"Updated task: {task.id}")

