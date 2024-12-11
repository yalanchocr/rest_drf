from myapp.serializers import TaskSerializer
from myapp.models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from myapp.customPagination import CustomPageNumberPagination


class TaskAPIView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk=None):
        queryset = Task.objects.filter(user=request.user)
        if pk:
            try:
                product = queryset.get(q_task_id=pk)
                serializer = TaskSerializer(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = TaskSerializer(paginated_queryset, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
