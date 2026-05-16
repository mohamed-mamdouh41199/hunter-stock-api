from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockItemViewSet

router = DefaultRouter()
router.register(r'items', StockItemViewSet, basename='stock-item')

urlpatterns = [
    path('', include(router.urls)),
]
