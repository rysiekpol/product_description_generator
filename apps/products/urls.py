from django.urls import path
from rest_framework import routers

from apps.products import views

from .views import (
    DescriptionViewSet,
    MySharesView,
    ProductsAPIView,
    ProductViewSet,
    ShareView,
    TranslateView,
)

urlpatterns = [
    path(
        "search/<str:name>/", ProductsAPIView.as_view(), name="product_search_details"
    ),
    path(
        "images/<str:uuid_name>/",
        views.serve_product_image,
        name="serve_image",
    ),
    path("translate/", TranslateView.as_view(), name="translate_description"),
    path("share/", ShareView.as_view(), name="share_product"),
    path("my_shares/", MySharesView.as_view(), name="share_product"),
]

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"description", DescriptionViewSet, basename="description")

urlpatterns += router.urls
