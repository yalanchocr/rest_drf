import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toturial2.settings')

application = get_wsgi_application()


from django_q.tasks import async_task


from myapp.queue_task import my_task

async_task(my_task, "a", "aa")