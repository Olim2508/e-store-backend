from rest_framework import viewsets

from main.models import ProductCategory, Product
from main.paginators import BasePageNumberPagination
from main.serializers import ProductCategorySerializer, ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all().order_by("-id")
    pagination_class = BasePageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-id")
    pagination_class = BasePageNumberPagination

