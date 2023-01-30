from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import ApiCalls

app_name = "main"

router = DefaultRouter()
router.register("category", views.ProductCategoryViewSet, basename="category")
router.register("product", views.ProductViewSet, basename="product")

urlpatterns = [
    path("order/create/", views.OrderCreate.as_view({"post": "create"}), name='order_create'),
    path('test/caching/', ApiCalls.as_view(), name='api_results'),
]

urlpatterns += router.urls
