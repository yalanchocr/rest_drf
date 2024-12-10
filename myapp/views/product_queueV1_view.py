from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_q.tasks import async_task

from myapp.serializers import ProductSerializer, ProductSerializer2
from myapp.import_data.import_product import import_products
from .upload_file_views import upload_file_view
from myapp.models import Task
from django.db import transaction

class UploadDataView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            async_task(import_products, serializer.validated_data)
            return Response({'message': 'Data import task started'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadDataView2(APIView):
    def post(self, request, format=None):
        # serializer = ProductSerializer(data=request.data)
        serializer = ProductSerializer2(data=request.data, context={'request': request})
        domain = request.get_host()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def upload_task(task_id, user, *args, **kwargs):
    task = Task.objects.get(id=task_id)
    try:
        file = task.file
        print(f"do import file size {file.size} ")
        with transaction.atomic():
            pass

    except Exception as err:
        task.set_status_failed("failled because use ...")
    else:
        task.set_status_successful()


class UploadDataQueue(APIView):
    def post(self, request,  *args, **kwargs):
        return upload_file_view(upload_task, request, *args, **kwargs)

    # def post(self, request):  #     serializer = ProductSerializer(data=request.data)  #     if serializer.is_valid():  #         product = serializer.save()  #         return Response({'message': 'Data import task started'}, status=status.HTTP_201_CREATED)  #     else:  #         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
