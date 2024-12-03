from django_q.tasks import async_task
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from myapp.helpers.constants import MESSAGES as MSG
from myapp.models import Task

def upload_file_view(task_func, request, *args, **kwargs):
    try:
        file = request.FILES["file"]
        if file.size > 20: # 20 mb
            raise ValidationError(MSG.FILE_SIZE_NOT_VALID)

        task = Task.objects.create(file=file, user=request.user, type=Task.IMPORT_TYPE, title=file.name)
        q_task_id = async_task(task_func, task.id, request.user, *args, **kwargs)
        Task.objects.filter(id=task.id).update(q_task_id=q_task_id)

        return Response({'task_id':q_task_id})

    except KeyError:
        raise ValidationError(MSG.FILE_NOT_PROVIDED)
