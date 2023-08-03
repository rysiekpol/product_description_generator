import mimetypes
import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, ProductDescriptions, ProductImage
from .permissions import IsProductAuthorOrReadOnly
from .serializers import (
    CreateDescriptionSerializer,
    CreateProductSerializer,
    ProductSerializer,
    TranslateTextSerializer,
)
from .tasks import start_async_translation

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


class DescriptionViewSet(viewsets.ModelViewSet):
    """
    An endpoint for creating a product description.
    """

    serializer_class = CreateDescriptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProductDescriptions.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(product__created_by=self.request.user)
        return queryset


class TranslateView(CreateAPIView):
    """
    An endpoint for translating text.
    """

    serializer_class = TranslateTextSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Translate the text.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        description_id = serializer.validated_data["description_id"]
        languages = serializer.validated_data["languages"]

        description = get_object_or_404(ProductDescriptions, id=description_id)
        text = description.description

        start_async_translation(text, request, languages)

        return Response(
            {"detail": "Mail with translations will be sent after task is completed"},
            status=status.HTTP_200_OK,
        )


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
