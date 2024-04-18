from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'wss/chat/(?P<username>\w+)_(?P<username2>\w+)_chatroom/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<family_name>\w+)_chatroom/$', consumers.FamilyChatConsumer.as_asgi()),
]