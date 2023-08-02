from pathlib import PurePath

from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import serializers

from .models import Product, ProductDescriptions, ProductImage
from .services import Operation
from .tasks import start_async_tasks


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize ProductImage model.
    """

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "image_url")

    def get_image_url(self, obj):
        """
        Returns the URL of the image.
        """
        request = self.context["request"]
        product_url_path = reverse(
            "serve_image",
            kwargs={"uuid_name": PurePath(obj.image.url).stem},
        )

        return request.build_absolute_uri(product_url_path)


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
        product = Product(**validated_data)

        images = [
            ProductImage(product=product, image=image, original_filename=image.name)
            for image in uploaded_images
        ]

        product.save()

        ProductImage.objects.bulk_create(images)

        return product


class CreateDescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer class to create ProductDescriptions model.
    """

    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductDescriptions
        fields = ("id", "product", "description", "product_id")
        read_only_fields = ("id", "description", "product")

    def create(self, validated_data):
        # Create descriptions
        try:
            request = self.context["request"]
            product = get_object_or_404(Product, id=validated_data["product_id"])
            if product.created_by != request.user:
                raise serializers.ValidationError(
                    "You are not authorized to create a description for this product."
                )

            start_async_tasks(request, product, Operation.CREATED)
        except serializers.ValidationError as e:
            raise e

        except Exception as e:
            # If there is an error in creating the description, delete the product and raise an error
            product.delete()
            raise serializers.ValidationError(
                f"Error creating product description: {e}"
            )

        return validated_data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        # Update descriptions
        try:
            request = self.context["request"]
            if instance.product.created_by != request.user:
                raise serializers.ValidationError(
                    "You are not authorized to update a description for this product."
                )

            start_async_tasks(request, instance, Operation.UPDATED)
        except serializers.ValidationError as e:
            raise e

        except Exception as e:
            raise serializers.ValidationError(
                f"Error updating product description: {e}"
            )

        return instance
