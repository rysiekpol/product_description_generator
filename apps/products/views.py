import mimetypes
import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Product, ProductDescriptions, ProductImage, SharedProducts
from .permissions import IsProductAuthorOrReadOnly
from .serializers import (
    CreateDescriptionSerializer,
    CreateProductSerializer,
    ProductSerializer,
    SharedProductsSerializer,
    TranslateTextSerializer,
)
from .tasks import send_description_update, start_async_translation

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """

    permission_classes = [IsProductAuthorOrReadOnly, IsAuthenticated]
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CreateProductSerializer
        return ProductSerializer


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


class ShareView(CreateAPIView):
    """
    An endpoint for sharing a product.
    """

    serializer_class = SharedProductsSerializer
    permission_classes = [IsAuthenticated]


class MySharesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    lookup_field = "shared_with"

    def get_queryset(self):
        return self.request.user.shared_by_others.all()


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
