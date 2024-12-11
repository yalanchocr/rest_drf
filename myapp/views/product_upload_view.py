from rest_framework.views import APIView
from myapp.import_data.upload_file_handler import upload_file_view, upload_task





class UploadDataQueue(APIView):
    def post(self, request,  *args, **kwargs):
        return upload_file_view(upload_task, request, *args, **kwargs)

