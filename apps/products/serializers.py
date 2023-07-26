import os

import requests
from rest_framework import serializers

from .models import Product, ProductDescriptions, ProductImage

MAX_N = 3
MAX_WORDS = 800


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize ProductImage model.
    """

    class Meta:
        model = ProductImage
        fields = ("id", "image")


class ProductDescriptionsSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize ProductDescriptions model.
    """

    class Meta:
        model = ProductDescriptions
        fields = ("id", "description")
        read_only_fields = ("id", "description")


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Product model.
    """

    images = ProductImageSerializer(many=True, read_only=True)
    descriptions = ProductDescriptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
            "images",
            "descriptions",
        )
        read_only_fields = ("created_at", "updated_at", "id", "created_by")


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to create Product model.
    Up to 5 images can be added to the product.
    """

    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        max_length=5,
    )
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(max_length=500, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
            "images",
            "uploaded_images",
            "description",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        n = int(self.context["request"].query_params.get("n", 1))
        words = int(self.context["request"].query_params.get("words", 400))

        n = min(n, MAX_N)
        words = min(words, MAX_WORDS)

        # Create images
        for image in uploaded_images:
            try:
                ProductImage.objects.create(product=product, image=image)
            except Exception as e:
                # If there is an error in creating an image, delete the product and raise an error
                product.delete()
                raise serializers.ValidationError(f"Error creating product image: {e}")

        # Create descriptions
        try:
            combined_tags = product.describe_product_images()
            description = product.generate_product_description(combined_tags, n, words)
            ProductDescriptions.objects.create(product=product, description=description)
        except Exception as e:
            # If there is an error in creating the description, delete the product and raise an error
            product.delete()
            raise serializers.ValidationError(
                f"Error creating product description: {e}"
            )

        return product

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        n = int(self.context["request"].query_params.get("n", 1))
        words = int(self.context["request"].query_params.get("words", 400))

        n = min(n, MAX_N)
        words = min(words, MAX_WORDS)

        # Update descriptions
        try:
            combined_tags = instance.describe_product_images()
            description = instance.generate_product_description(combined_tags, n, words)
            ProductDescriptions.objects.create(
                product=instance, description=description
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Error updating product description: {e}"
            )

        return instance
