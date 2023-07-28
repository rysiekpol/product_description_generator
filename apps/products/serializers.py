from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Product model.
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "id", "created_by")


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to create Product model.
    """

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "id", "created_by")
