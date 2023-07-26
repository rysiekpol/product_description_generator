import os

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Product, ProductImage
from .permissions import IsProductAuthorOrReadOnly
from .serializers import CreateProductSerializer, ProductSerializer

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
    permission_classes = [AllowAny]


class AllProductsAPIView(ListAPIView):
    """
    An endpoint for getting all products.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()


def serve_product_image(request, pk):
    """
    A view to serve product images.
    """

    image = get_object_or_404(ProductImage, pk=pk)

    image_path = str(settings.BASE_DIR) + image.image.url

    response = FileResponse(open(image_path, "rb"))

    response["Content-Type"] = f"image/{image.image.name.split('.')[-1]}"
    response["Content-Length"] = os.path.getsize(image_path)

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{image.original_filename}"'

    return response
