from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'', views.ProductViewSet)  # Changed from 'products' to ''

app_name = 'products'

urlpatterns = [
    path('', include(router.urls)),
]