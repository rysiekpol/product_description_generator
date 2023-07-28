from django.urls import path, re_path
from rest_framework import routers

from .views import ProductsAPIView, ProductViewSet

urlpatterns = [
    path("search/<str:name>", ProductsAPIView.as_view(), name="product-search"),
]

router = routers.DefaultRouter()
router.register(r"", ProductViewSet, basename="product")

urlpatterns += router.urls
