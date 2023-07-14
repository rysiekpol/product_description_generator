from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product
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
