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


# file will be named as a product name and a number of image
def name_file(instance, filename):
    return f'products/{str(instance.product.name).lower().replace(" ", "_")}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    # path to image
    image = models.ImageField(upload_to=name_file, blank=True, null=True)
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
