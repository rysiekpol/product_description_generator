# Generated by Django 4.2.3 on 2023-08-04 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_productimage_original_filename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid_name',
            field=models.UUIDField(editable=False, null=True, unique=True),
        ),
    ]