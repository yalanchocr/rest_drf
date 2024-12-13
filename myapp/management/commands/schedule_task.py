from django.core.management.base import BaseCommand
from myapp.cron.func import schedule_task

class Command(BaseCommand):
    help = 'Schedules the check_task_pending task to run every 20 hours'

    def handle(self, *args, **kwargs):
        try:
            schedule_task()
            self.stdout.write(self.style.SUCCESS('Successfully scheduled the task.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error scheduling the task: {e}'))