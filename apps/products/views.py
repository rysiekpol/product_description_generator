import mimetypes
import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductImage
from .permissions import IsProductAuthorOrReadOnly
from .serializers import CreateProductSerializer, ProductSerializer

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """

    permission_classes = [IsProductAuthorOrReadOnly, IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
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


@permission_classes([IsAuthenticated, IsProductAuthorOrReadOnly])
def serve_product_image(request, uuid_name):
    """
    A view to serve product images.
    """

    image = get_object_or_404(ProductImage, image__contains=uuid_name)
    image_path = Path(settings.BASE_DIR, image.image.url.lstrip("/"))
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
