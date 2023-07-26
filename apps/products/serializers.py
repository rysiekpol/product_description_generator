from django.urls import reverse
from rest_framework import serializers

from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize ProductImage model.
    """

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image_url",
        )

    def get_image_url(self, obj):
        """
        Returns the URL of the image.
        """
        return reverse(
            "serve_image",
            kwargs={"pk": obj.id},
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Product model.
    """

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
            "images",
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
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product(**validated_data)

        images = [
            ProductImage(product=product, image=image) for image in uploaded_images
        ]

        for i in range(len(images)):
            images[i].original_filename = uploaded_images[i].name

        product.save()

        ProductImage.objects.bulk_create(images)

        return product
