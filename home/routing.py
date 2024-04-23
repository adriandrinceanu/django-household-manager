from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'wss/chat/(?P<username>\w+)_(?P<username2>\w+)_chatroom/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'wss/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'wss/chat/(?P<family_name>\w+)_chatroom(?P<family_id>\w+)/$', consumers.FamilyChatConsumer.as_asgi()),
]