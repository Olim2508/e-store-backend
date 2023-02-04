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
    path("comment/list/<int:product_id>/", views.CommentViewSet.as_view({"get": "list"}), name='comment_list'),
    path("comment/action/", views.CommentViewSet.as_view({"post": "comment_action"}), name='comment_action'),
]

urlpatterns += router.urls
