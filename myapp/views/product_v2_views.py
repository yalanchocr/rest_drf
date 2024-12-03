from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from myapp.models import Product
from myapp.serializers import ProductSerializer, ProductCreateUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from myapp.paginitions import MyPagination


class ProductListAPIView3(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Filter by name and in_stock status
        name = request.query_params.get('name')
        in_stock = request.query_params.get('in_stock')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if in_stock:
            queryset = queryset.filter(in_stock=in_stock)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView2(APIView):
    permission_classes = [IsAuthenticated]  # Optional authentication for entire view

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Creates a new product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCreateUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Updates an existing product
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
