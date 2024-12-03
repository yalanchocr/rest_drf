from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.queue_task import my_task

class ProductListAPIView2(APIView):
    permission_classes = [IsAuthenticated]  # Optional authentication for entire view


    def post(self, request):
        pass
        from django_q.tasks import async_task
        # async_task(my_task, arg1, arg2)

