from django.urls import path, re_path

from apps.products import views

urlpatterns = [
    path("search/<str:name>", views.ProductsAPIView.as_view(), name="products_details"),
    path(
        "details/<int:pk>/",
        views.CertainProductAPIView.as_view(),
        name="certain_product_details",
    ),
    path("details", views.AllProductsAPIView.as_view(), name="all_products"),
    path("create/", views.ProductCreateAPIView.as_view(), name="product_create"),
    path(
        "update/<int:pk>/", views.ProductUpdateAPIView.as_view(), name="product_update"
    ),
]
