from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "main"

router = DefaultRouter()
router.register("category", views.ProductCategoryViewSet, basename="category")
router.register("product", views.ProductViewSet, basename="product")

urlpatterns = [
    path("order/create/", views.OrderViewSet.as_view({"post": "create"}), name='order_create'),
    path("comment/create/", views.CommentViewSet.as_view({"post": "create"}), name='comment_create'),
]

urlpatterns += router.urls
