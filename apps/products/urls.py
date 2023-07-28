from django.urls import path
from rest_framework import routers

from apps.products import views

from .views import ProductsAPIView, ProductViewSet

urlpatterns = [
    path(
        "search/<str:name>/", ProductsAPIView.as_view(), name="product_search_details"
    ),
    path(
        "images/<str:uuid_name>/",
        views.serve_product_image,
        name="serve_image",
    ),
]

router = routers.DefaultRouter()
router.register(r"", ProductViewSet, basename="product")

urlpatterns += router.urls
