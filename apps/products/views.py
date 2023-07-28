import mimetypes
import os

import requests
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product, ProductDescriptions, ProductImage
from .permissions import IsProductAuthorOrReadOnly
from .serializers import (
    CreateProductSerializer,
    ProductDescriptionsSerializer,
    ProductSerializer,
)

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """

    permission_classes = [IsProductAuthorOrReadOnly, IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class ProductsAPIView(ListAPIView):
    """
    An endpoint for getting products by name.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProductAuthorOrReadOnly]

    def get_queryset(self):
        name = self.kwargs["name"]
        return Product.objects.filter(name__icontains=name)


def serve_product_image(request, pk):
    """
    A view to serve product images.
    """

    image = get_object_or_404(ProductImage, pk=pk)

    image_path = os.path.join(settings.BASE_DIR, image.image.url.lstrip("/"))

    response = FileResponse(open(image_path, "rb"))

    # Get the mimetype and encoding of the image file
    mime_type, _ = mimetypes.guess_type(image.image.url)

    # If the mimetype could not be guessed then default it to 'application/octet-stream'
    if mime_type is None:
        mime_type = "application/octet-stream"

    response["Content-Type"] = mime_type
    response["Content-Length"] = os.path.getsize(image_path)

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{image.original_filename}"'

    return response
