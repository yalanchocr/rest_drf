from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import Product
from myapp.serializers import ProductSerializer
from myapp.customPagination import CustomPageNumberPagination

class ProductAPIView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request, pk=None):
        queryset = Product.objects.all()
        name = request.query_params.get('name', None)
        in_stock = request.query_params.get('in_stock', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if in_stock is not None:
            in_stock = in_stock.lower() == 'true'
            queryset = queryset.filter(in_stock=in_stock)

        if pk:
            try:
                product = queryset.get(pk=pk)
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = queryset.order_by('-created_at')
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = ProductSerializer(paginated_queryset, many=True,  context={'request': request})
            return paginator.get_paginated_response(serializer.data)
            # return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class ProductListView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilter
#
#
# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilter




