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
    # field to store the original filename
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
