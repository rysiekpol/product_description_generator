from django.db import models

from apps.users.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # path to image
    image = models.CharField(max_length=128, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
