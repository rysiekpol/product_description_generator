import os
from pathlib import Path
from uuid import uuid4

import requests
from django.conf import settings
from django.db import models

from apps.users.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def describe_product_images(self):
        api_key = os.environ.get("API_KEY")
        api_secret = os.environ.get("API_SECRET")
        combined_tags = set()
        for image in self.images.all():
            image_path = str(settings.BASE_DIR) + image.image.url
            try:
                response = requests.post(
                    "https://api.imagga.com/v2/tags",
                    auth=(api_key, api_secret),
                    files={"image": open(image_path, "rb")},
                )
                response_data = response.json()

                # Extract the 3 most confident tags from the response
                tags = response_data["result"]["tags"][:3]
                tag_names = [tag["tag"]["en"] for tag in tags]
            except requests.RequestException as e:
                return f"HTTP Request failed: {e}"

            combined_tags.update(tag_names)
        return list(combined_tags)

    def generate_product_description(self, tags, n, words):
        api_key = os.environ.get("GPT_API_KEY")
        endpoint = "https://api.openai.com/v1/chat/completions"

        prompt = f"Generate a product description for a {self.name} which has tags: {', '.join(tags)}"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "max_tokens": words,
            "n": n,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        try:
            response = requests.post(endpoint, json=data, headers=headers)
            response_data = response.json()

            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                return "Product description generation failed."

        except requests.RequestException as e:
            return f"HTTP Request failed: {e}"

    def __str__(self):
        return self.name


def name_file(instance, filename):
    new_filename = f"{uuid4()}{Path(filename).suffix}"
    return Path(settings.MEDIA_PRODUCTS_ROOT) / Path(new_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    # path to image
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    # path to image
    image = models.ImageField(upload_to=name_file, blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"


class ProductDescriptions(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="descriptions",
    )
    description = models.TextField()

    def __str__(self):
        return f"{self.product.name} - {self.description}"
