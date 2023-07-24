import os

import requests
from rest_framework import serializers

from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize ProductImage model.
    """

    class Meta:
        model = ProductImage
        fields = "__all__"


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
        # read_only_fields = ("created_at", "updated_at", "id", "created_by")

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        if uploaded_images:
            image_url = uploaded_images[0].image

            api_key = os.environ.get("API_KEY")
            api_secret = os.environ.get("API_SECRET")
            imagga_tags_url = f"https://api.imagga.com/v2/tags?image_url={image_url}"
            headers = {"Authorization": f"Basic {api_key}:{api_secret}"}

            try:
                response = requests.get(imagga_tags_url, headers=headers)
                response_data = response.json()

                # Extract the 5 most confident tags from the response
                tags = response_data["result"]["tags"][:5]
                tag_names = [tag["tag"]["en"] for tag in tags]

                # Update the product instance with description and tags
                product.description = f"Tags: {', '.join(tag_names)}"
                product.tags = tag_names
                product.save()

            except requests.RequestException:
                # Handle any errors that might occur during the API request
                pass

        return product
