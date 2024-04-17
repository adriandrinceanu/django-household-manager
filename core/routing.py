from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, include

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            path("", include("home.routing")),
            # home.routing.websocket_urlpatterns  # use home app's websocket_urlpatterns
        ),
    ),
})