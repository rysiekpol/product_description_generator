from django.urls import path

from .consumers import ProductDescriptionConsumer

websocket_urlpatterns = [
    path("ws/descriptions/<int:product_id>/", ProductDescriptionConsumer.as_asgi()),
]
