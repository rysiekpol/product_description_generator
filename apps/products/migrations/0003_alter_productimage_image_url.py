# Generated by Django 4.2.3 on 2023-07-14 11:38

import apps.products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_image_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image_url',
            field=models.ImageField(unique=True, upload_to=apps.products.models.name_file),
        ),
    ]
