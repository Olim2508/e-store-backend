from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'main'

router = DefaultRouter()
router.register('category', views.ProductCategoryViewSet, basename='category')

urlpatterns = [

]

urlpatterns += router.urls
