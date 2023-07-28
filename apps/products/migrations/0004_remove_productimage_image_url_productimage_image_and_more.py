# Generated by Django 4.2.3 on 2023-07-14 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productimage_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='image_url',
        ),
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product'),
        ),
    ]
