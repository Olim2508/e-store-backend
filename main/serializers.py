from rest_framework import serializers

from main.models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"
