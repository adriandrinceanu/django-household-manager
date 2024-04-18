from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
import logging
from django.contrib.humanize.templatetags.humanize import naturaltime


logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"notifications_{self.user.id}"
        logger.info(f"Connecting to group {self.group_name}")

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting from group {self.group_name}")
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    @database_sync_to_async
    def get_notifications(self):
        from home.models import Notification
        # Get the current user's family
        current_user_family = self.user.member.family
        # Fetch notifications for the current user's family
        notifications = Notification.objects.filter(family=current_user_family)
        notifications_json = []

        for notification in notifications:
            notifications_json.append({
                'id': notification.id,
                'user': notification.user.username if notification.user else None,
                'message': notification.message,
                'is_read': notification.is_read,
                'created_at': str(naturaltime(notification.created_at)),
                'family': notification.family.name if notification.family else None,
                'member': {
                    'id': notification.member.id,
                    'name': notification.member.name,
                    'profile_pic': notification.member.profile_pic.url if notification.member.profile_pic else None,
                } if notification.member else None,
                'chore': {
                    'id': notification.chore.id,
                    'title': notification.chore.title,
                } if notification.chore else None,
            })

        logger.info(f"Got {len(notifications_json)} notifications")
        return notifications_json
    
    # Receive message from WebSocket
    async def receive_json(self, content):
        command = content.get("command", None)
        if command == "get_notifications":
            logger.info("Received get_notifications command")
            notifications = await self.get_notifications()
        await self.send_json({"notifications": notifications})
    

    

    # Receive message from room group
    async def send_notification(self, event):
        logger.info(f"Sending notification: {event['text']}")
        await self.send_json(event["text"])