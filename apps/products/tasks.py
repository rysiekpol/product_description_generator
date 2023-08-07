from __future__ import absolute_import, unicode_literals

import json

import requests
from asgiref.sync import async_to_sync
from celery import chain, shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .models import Product, ProductDescriptions
from .services import Operation, describe_product_images, generate_product_description

MAX_N = 3
MAX_WORDS = 800


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


@shared_task
def send_email_translation_task(
    result_from_previous_task, subject, from_email, to_email
):
    send_mail(
        subject=subject,
        message=result_from_previous_task.encode("utf-8").decode("unicode-escape"),
        from_email=from_email,
        recipient_list=[to_email],
    )


@shared_task
def translate_text_task(text, languages, n, words):
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": text,
        "languages": languages,
        "n": n,
        "words": words,
    }
    response = requests.post(settings.FAST_API_URL, json=payload, headers=headers)

    return response.json()


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
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=product.created_by.email,
        ),
    ).apply_async()


def start_async_translation(text, request, languages):
    n = int(request.query_params.get("n", 1))
    words = int(request.query_params.get("words", 400))

    n = min(n, MAX_N)
    words = min(words, MAX_WORDS)

    chain(
        translate_text_task.s(text, languages, n, words),
        send_email_translation_task.s(
            subject=f"Your translation is ready",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=request.user.email,
        ),
    ).apply_async()
