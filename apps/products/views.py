import os

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product, ProductDescriptions
from .permissions import IsProductAuthorOrReadOnly
from .serializers import (
    CreateProductSerializer,
    ProductDescriptionsSerializer,
    ProductSerializer,
)

# Create your views here.


class CertainProductAPIView(RetrieveUpdateAPIView):
    """
    An endpoint for getting and updating certain product.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsProductAuthorOrReadOnly, IsAuthenticated]
    queryset = Product.objects.all()


class ProductsAPIView(ListAPIView):
    """
    An endpoint for getting products by name.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs["name"]
        return Product.objects.filter(name__icontains=name)


class ProductCreateAPIView(CreateAPIView):
    """
    An endpoint for creating product.
    """

    parser_class = [MultiPartParser, FormParser]
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated]


class AllProductsAPIView(ListAPIView):
    """
    An endpoint for getting all products.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    """
    An endpoint for updating product.
    """

    parser_class = [MultiPartParser, FormParser]
    serializer_class = CreateProductSerializer
    permission_classes = [IsProductAuthorOrReadOnly, IsAuthenticated]
    queryset = Product.objects.all()


class ProductDescriptionsAPIView(ListAPIView):
    """
    An endpoint for creating description for product.
    """

    serializer_class = ProductDescriptionsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        api_key = os.environ.get("API_KEY")
        api_secret = os.environ.get("API_SECRET")

        try:
            product = get_object_or_404(Product, id=kwargs.get("pk"))
            combined_tags = set()

            for image in product.images.all():
                image_path = str(settings.BASE_DIR) + image.image.url

                response = requests.post(
                    "https://api.imagga.com/v2/tags",
                    auth=(api_key, api_secret),
                    files={"image": open(image_path, "rb")},
                )
                response_data = response.json()

                # Extract the 3 most confident tags from the response
                tags = response_data["result"]["tags"][:3]
                tag_names = [tag["tag"]["en"] for tag in tags]

                combined_tags.update(tag_names)

            description = f"Tags: {', '.join(combined_tags)}"
            ProductDescriptions.objects.create(product=product, description=description)

        except requests.RequestException:
            return Response(
                "HTTP Request failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_200_OK)
