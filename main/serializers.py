from typing import List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import Product, ProductCategory, Order, OrderDetail
from main.services import ProductService, OrderService, CommentService


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
        ret.update(
            {
                "category": {
                    "id": category.id,
                    "title": category.title,
                }
            }
        )
        return ret


class OrderDetailSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.Serializer):
    orders = serializers.ListField(child=OrderDetailSerializer())

    def validate(self, data):
        for item in data['orders']:
            if not ProductService.is_product_exists(item['product_id']):
                raise ValidationError({"product_id": f"Product id {item['product_id']} doesn't exists"})
        return data

    def save(self, **kwargs):
        data: List[dict] = self.validated_data['orders']
        user = self.context['request'].user
        OrderService.create_bulk_order_details(Order(user=user), data)


class CommentSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True, write_only=True)
    text = serializers.CharField(required=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    def validate(self, data):
        if not ProductService.is_product_exists(data['product_id']):
            raise ValidationError({"product_id": f"Product id {data['product_id']} doesn't exists"})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        comment = CommentService.create_comment(validated_data, user)
        return comment
