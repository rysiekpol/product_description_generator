from channels.routing import ProtocolTypeRouter, URLRouter

import apps.products.routing

application = ProtocolTypeRouter(
    {"websocket": URLRouter(apps.products.routing.websocket_urlpatterns)}
)
