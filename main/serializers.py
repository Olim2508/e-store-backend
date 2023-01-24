from rest_framework import serializers

from main.models import ProductCategory, Product
from main.services import ProductService


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategory()

    class Meta:
        model = Product
        fields = ["id", "name", "category", "price"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        category = ProductService.get_category(instance.category_id)
        ret.update({
            "category": {
                "id": category.id,
                "title": category.title,
            }
        })
        return ret

