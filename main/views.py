from rest_framework import viewsets

from main.filters import ProductFilter
from main.models import Product, ProductCategory
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
    filterset_class = ProductFilter
