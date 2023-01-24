from rest_framework import viewsets

from main.models import ProductCategory
from main.paginators import BasePageNumberPagination
from main.serializers import ProductCategorySerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    pagination_class = BasePageNumberPagination

