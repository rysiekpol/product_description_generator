from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail

from .models import Product, ProductDescriptions
from .services import describe_product_images, generate_product_description


@shared_task
def describe_product_images_task(product_id):
    product = Product.objects.get(id=product_id)
    return describe_product_images(product)


@shared_task
def generate_product_description_task(tags, product_id, n, words):
    product = Product.objects.get(id=product_id)
    description = generate_product_description(product, tags, n, words)
    ProductDescriptions.objects.create(product=product, description=description)


@shared_task
def send_email_task(result_from_previous_task, subject, message, from_email, to_email):
    send_mail(subject, message, from_email, [to_email])
