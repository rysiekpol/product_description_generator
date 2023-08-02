from __future__ import absolute_import, unicode_literals

from asgiref.sync import async_to_sync
from celery import chain, shared_task
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.urls import reverse

from .models import Product, ProductDescriptions
from .services import Operation, describe_product_images, generate_product_description

MAX_N = 3
MAX_WORDS = 800


def send_description_update(product_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"product_{product_id}", {"type": "description_update", "message": message}
    )


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
def send_email_task(
    result_from_previous_task, subject, message, from_email, to_email, product_id
):
    # send the notification
    send_description_update(product_id, "Description generation completed!")
    send_mail(subject, message, from_email, [to_email])


def start_async_tasks(request, product, operation):
    n = int(request.query_params.get("n", 1))
    words = int(request.query_params.get("words", 400))

    n = min(n, MAX_N)
    words = min(words, MAX_WORDS)

    product_url_path = reverse("product-detail", kwargs={"pk": product.id})
    product_url = request.build_absolute_uri(product_url_path)

    chain(
        describe_product_images_task.s(product.id),
        generate_product_description_task.s(product.id, n, words),
        send_email_task.s(
            subject=f"Product {operation.value}",
            message=f"Your product has been successfully {operation.value}. You can see the description in {product_url}",
            from_email="no-reply@masze.pl",
            to_email=product.created_by.email,
            product_id=product.id,
        ),
    ).apply_async()
