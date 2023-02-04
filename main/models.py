from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.ForeignKey(
        "main.ProductCategory", on_delete=models.CASCADE, related_name="product"
    )

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} + {self.user}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        "main.Order", on_delete=models.CASCADE, related_name="order_detail"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.id}, order_id={self.order.id}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.id} - {self.user}"

    class Meta:
        ordering = ['-id']


