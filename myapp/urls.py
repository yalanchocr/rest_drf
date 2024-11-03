from django.urls import path, include
from rest_framework import routers
from .views import ProductListView, ProductDetailView, ProductViewSet, ProductAPIView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
]
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('products/', ProductListView.as_view(), name='product-list'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
# ]