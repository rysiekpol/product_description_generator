from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product
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
        return Product.objects.filter(name__icontains=name).filter(
            created_by=self.request.user
        )
