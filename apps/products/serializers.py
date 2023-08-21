from datetime import timedelta
from pathlib import PurePath

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from .models import Product, ProductDescriptions, ProductImage, SharedProducts
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

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.images.all().delete()

        uploaded_images = validated_data.pop("uploaded_images")
        images = [
            ProductImage(product=instance, image=image, original_filename=image.name)
            for image in uploaded_images
        ]

        ProductImage.objects.bulk_create(images)

        return instance


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


class TranslateTextSerializer(serializers.Serializer):
    """
    Serializer class to translate text.
    """

    description_id = serializers.IntegerField(write_only=True)
    languages = serializers.ListField(child=serializers.CharField(), max_length=5)

    class Meta:
        fields = ("description_id", "languages")


class SharedProductsSerializer(serializers.ModelSerializer):
    """
    Serializer class to share a product.
    """

    product_id = serializers.IntegerField(write_only=True)
    user_email = serializers.EmailField(write_only=True)
    share_time = serializers.DurationField(write_only=True)

    class Meta:
        model = SharedProducts
        fields = ("product_id", "user_email", "share_time")

    def validate_user_email(self, value):
        """
        Check that the product owner is not the same as the user sharing the product.
        """

        user = get_object_or_404(get_user_model(), email=value)
        if user == self.context["request"].user:
            raise serializers.ValidationError(
                "You cannot share a product with yourself."
            )
        return value

    def validate_product_id(self, value):
        """
        Check that the user sharing the product is the product owner.
        """
        product = get_object_or_404(Product, id=value)

        if product.created_by != self.context["request"].user:
            raise serializers.ValidationError(
                "You are not authorized to share this product."
            )
        return value

    def validate_share_time(self, value):
        """
        Check that the share time is between one second and one week.
        """
        one_second = timedelta(seconds=1)
        one_week = timedelta(weeks=1)

        if not one_second <= value <= one_week:
            raise serializers.ValidationError(
                "Share time must be between one second and one week."
            )
        return value

    def validate(self, data):
        """
        Check that the product is not already shared with the user.
        """
        product = get_object_or_404(Product, id=data["product_id"])
        user = get_object_or_404(get_user_model(), email=data["user_email"])

        if SharedProducts.objects.filter(
            product=product, shared_with=user, shared_by=self.context["request"].user
        ).exists():
            raise serializers.ValidationError(
                "This product is already shared with this user."
            )
        return data

    def create(self, validated_data):
        # Create shared product
        try:

            print(validated_data)
            print("test2")
            request = self.context["request"]
            product = get_object_or_404(Product, id=validated_data["product_id"])
            shared_with = get_object_or_404(
                get_user_model(), email=validated_data["user_email"]
            )
            print("test")
            print(validated_data["share_time"])

            SharedProducts.objects.create(
                product=product,
                shared_by=request.user,
                shared_with=shared_with,
                expiration_time=timezone.now() + validated_data["share_time"],
            )

        except serializers.ValidationError as e:
            raise e

        except Exception as e:
            raise serializers.ValidationError(f"Error sharing product: {e}")

        return validated_data
