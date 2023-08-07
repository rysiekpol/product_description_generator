# Generated by Django 4.2.3 on 2023-08-07 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_product_uuid_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration_time', models.DateTimeField(editable=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared', to='products.product')),
                ('shared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared', to=settings.AUTH_USER_MODEL)),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
