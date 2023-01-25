from typing import List

from django.db.models import Q
from django_filters import rest_framework as filters

from main.models import Product


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    category = NumberInFilter(method="category_ids_filter")
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(category__title__icontains=value)
        )

    def category_ids_filter(self, queryset, name, value: List[int]):
        return queryset.filter(category_id__in=value)

    class Meta:
        model = Product
        fields = ["search", "category", "price_min", "price_max"]
