from django.urls import path
from rest_framework import routers
from myapp.views.product_v1_views import ProductViewSet, ProductAPIView
from .views import UploadDataView, UploadDataView2, UploadDataQueue, TaskAPIView
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    path('products_queue', UploadDataView.as_view(), name='product-queue'),
    path('upload_product', UploadDataView2.as_view(), name='upload_product'),
    path('upload_product_file', UploadDataQueue.as_view(), name='upload_product_file'),
    path('tasks', TaskAPIView.as_view(), name='task_list'),
]
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('products/', ProductListView.as_view(), name='product-list'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
# ]