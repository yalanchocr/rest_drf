from myapp.serializers import TaskSerializer
from myapp.models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class TaskAPIView(APIView):
    def get(self, request):
        queryset = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)