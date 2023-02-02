from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.filters import ProductFilter
from main.models import Product, ProductCategory
from main.paginators import BasePageNumberPagination
from main.serializers import ProductCategorySerializer, ProductSerializer, OrderSerializer, CommentSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all().order_by("-id")
    pagination_class = BasePageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-id")
    pagination_class = BasePageNumberPagination
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True}, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
