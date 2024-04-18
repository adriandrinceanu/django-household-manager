from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
import logging
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime


logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        # Get the family id
        # Get the family id in a synchronous context
        family_id = await sync_to_async(self.get_family_id)()
        self.group_name = f"notifications_{family_id}"
        logger.info(f"Connecting to group {self.group_name}")
        
        

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        
    # Synchronous method to get family id
    def get_family_id(self):
        return self.user.member.family.id

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"Disconnecting from group {self.group_name}")
        
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
    
    async def new_notification(self, notification):
        # Send notification to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'notification': notification
            }
        )

    # Receive message from room group
    async def send_notification(self, event):
        notification = event['notification']
        # Send message to WebSocket
        await self.send_json({
        'notification': notification,
    })

    

    # # Receive message from room group
    # async def send_notification(self, event):
    #     logger.info(f"Sending notification: {event['text']}")
    #     await self.send_json(event["text"])
    
    
class FamilyChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_username(self):
        # Check if user information is already stored in the connection object
        if hasattr(self, 'user'):
            return self.user.username

        # If not stored, retrieve it from the database using sync_to_async
        from django.contrib.auth.models import User
        user = User.objects.get(pk=self.scope['user'].pk)
        return user.username
    
    async def connect(self):
        from .models import Message 
        self.room_name = self.scope['url_route']['kwargs']['family_name']
        self.room_group_name = f"chat_{self.room_name}"
        logger.info(f"Room group: {self.room_group_name}")
        # Accept the WebSocket connection
        await self.accept()
        
        # Load past messages from the database
        past_messages = await sync_to_async(Message.objects.filter)(chat_id=self.room_name)
        past_messages = await sync_to_async(list)(past_messages.order_by('timestamp'))
        

        
        for message in past_messages:
            # username = await self.get_username() #old username retrieval. it returned the current username of the logged user.
            username = message.username   # Get the username from the message
            timestamp = str(naturaltime(message.timestamp))  #Convert the timestamp to natural time
            await self.send(text_data=json.dumps({
                'message': message.content,
                'username': username,
                'timestamp': timestamp
            }))
        logger.info(f"Connected to {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Joined room group: {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Left room group: {self.room_group_name}")
    
        
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']  #Extract the username
        
        # Save the message to the database
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        logger.info(f"Received message: {message}")
        
    async def chat_message(self, event):
        # This method is called whenever a 'chat_message' is received
        message = event['message']
        # username = self.scope["user"].username # for selfkeeping
        username = event['username']
        now = datetime.now()
        
         # Humanize the timestamp
        timestamp = str(naturaltime(now))

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
        logger.info(f"Sending message: {message}")

        
        
    @sync_to_async
    def save_message(self, username, message):
        from .models import Message, Member

        try:
            # Get the member object using the username
            member = Member.objects.get(user__username=username)

            if member:
                # Access the user and family associated with the member
                self.user = self.scope["user"]
                family = member.family  # Get the family
                username = self.user.username
                # Save the message with the user and family
                Message.objects.create(user=self.user, family=family, username=username, content=message, chat_id=self.room_name)
            else:
                print("Error: Member not found for username", username)
        except Member.DoesNotExist:
            print("Error: Member not found for username", username)