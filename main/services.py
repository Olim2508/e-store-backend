from typing import List

from django.contrib.auth import get_user_model

from main.models import ProductCategory, Product, Order, OrderDetail, Comment
from main.utils import except_shell


User = get_user_model()

class ProductService:
    @staticmethod
    @except_shell((ProductCategory.DoesNotExist,))
    def get_category(id: int):
        return ProductCategory.objects.get(id=id)

    @staticmethod
    def is_product_exists(id: int):
        return Product.objects.filter(id=id).exists()

    @staticmethod
    @except_shell((Product.DoesNotExist,))
    def get_product_by_id(id: int):
        return Product.objects.get(id=id)


class OrderService:

    @staticmethod
    def create_bulk_order_details(order: Order, data: List[dict]):
        order_items = list()
        total_price = 0
        for item in data:
            product = ProductService.get_product_by_id(item['product_id'])
            price = item['quantity'] * product.price
            total_price += price
            order_items.append(
                OrderDetail(order=order, product=product, price=price, quantity=item['quantity'])
            )
        order.amount = total_price
        order.save()
        OrderDetail.objects.bulk_create(order_items)


class CommentService:

    @staticmethod
    def create_comment(data: dict, user: User):
        product = ProductService.get_product_by_id(data['product_id'])
        return Comment.objects.create(text=data['text'], user=user, product=product)