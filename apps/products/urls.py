from django.urls import path
from rest_framework import routers

from apps.products import views

from .views import DescriptionViewSet, ProductsAPIView, ProductViewSet

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
router.register(r"product", ProductViewSet, basename="product")
router.register(r"description", DescriptionViewSet, basename="description")

urlpatterns += router.urls
