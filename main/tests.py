from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from main.models import ProductCategory, Product, Order, OrderDetail, Comment

User = get_user_model()


@tag('order')
class OrderApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='rahmatovolim3@gmail.com', password=make_password('test1235'))
        self.user.save()
        self.product_category_1 = ProductCategory.objects.create(title="milk products")
        self.product_category_2 = ProductCategory.objects.create(title="drinks")
        self.product_category_3 = ProductCategory.objects.create(title="sweets")

        self.product_1 = Product.objects.create(name="Butter", category=self.product_category_1, price=200)
        self.product_2 = Product.objects.create(name="Coca cola", category=self.product_category_2, price=300)
        self.product_3 = Product.objects.create(name="Twix", category=self.product_category_3, price=100)
        self.product_4 = Product.objects.create(name="Fanta", category=self.product_category_2, price=250)

        url = reverse_lazy('auth_app:sign-in')
        data = {
            'email': 'rahmatovolim3@gmail.com',
            'password': 'test1235'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')

    def test_create_order(self):
        url = reverse_lazy('main:order_create')
        data = {
            "orders": [
                {"product_id": self.product_1.id, "quantity": 3},
                {"product_id": self.product_2.id, "quantity": 5},
                {"product_id": 10, "quantity": 4},
            ]
        }
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderDetail.objects.count(), 0)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        data['orders'][2]['product_id'] = self.product_3.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(response.json(), {"status": True}, response.content)
        order = Order.objects.first()
        order_items = OrderDetail.objects.filter(order=order)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order_items.count(), 3)
        self.assertEqual(order.user, self.user)
        self.assertTrue(OrderDetail.objects.filter(order=order, product=self.product_1).exists())


@tag("comment")
class CommentApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='rahmatovolim3@gmail.com', password=make_password('test1235'))
        self.user.save()
        self.product_category_1 = ProductCategory.objects.create(title="drinks")

        self.product_1 = Product.objects.create(name="Coca cola", category=self.product_category_1, price=300)
        self.product_2 = Product.objects.create(name="Fanta", category=self.product_category_1, price=250)

        url = reverse_lazy('auth_app:sign-in')
        data = {
            'email': 'rahmatovolim3@gmail.com',
            'password': 'test1235'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')

    def test_create_comment(self):
        url = reverse_lazy('main:comment_create')
        data = {"product_id": 100, "text": "Great product!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        data['text'] = ''
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        data['product_id'] = self.product_1.id
        data['text'] = 'Great product!'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Comment.objects.count(), 1)

    def test_get_comments(self):
        url = reverse_lazy('main:comment_create')
        data = {"product_id": self.product_1.id, "text": "Great product!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        data['text'] = 'comment 2 text'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

        url = reverse_lazy('main:comment_list', args=[self.product_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.json()), 2)
        url = reverse_lazy('main:comment_list', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(len(response.json()), 0)

    # def test_comment_like(self):
    #     pass
