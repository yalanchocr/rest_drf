from django.urls import path
from myapp.views.product_views import ProductAPIView
from .views import UploadDataQueue, TaskAPIView

urlpatterns = [
    path('products', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>', ProductAPIView.as_view(), name='product-detail'),
    path('upload_product_file', UploadDataQueue.as_view(), name='upload_product_file'),
    path('tasks', TaskAPIView.as_view(), name='task-list'),
    path('tasks/<str:pk>', TaskAPIView.as_view(), name='task-detail'),
]
