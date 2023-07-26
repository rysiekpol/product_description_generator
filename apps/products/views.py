import os

import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
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
