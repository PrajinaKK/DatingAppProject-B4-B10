
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger('registration')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("roommm", self.room_name)
        # logger.debug(f"Connected to room: {self.room_name}")

        # Join the chat room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self, close_code):
            
        # Leave the chat room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']
        receiver_id = data['receiver']

        # Get sender and receiver User objects
        sender = await self.get_user(sender_id)
        receiver = await self.get_user(receiver_id)

        # Get or create the chat room
        room_name = self._get_room_name(sender_id, receiver_id)
        chat_room, created = await self.get_chat_room(room_name)

        # Save message to the database
        chat_message = await self.create_chat_message(chat_room, sender, message)
        chat_message.save()

        # Send message to the chat room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )
        

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_chat_room(self, room_name):
        return ChatRoom.objects.get_or_create(name=room_name)

    @database_sync_to_async
    def create_chat_message(self, room, user, message):
        return ChatMessage.objects.create(room=room, user=user, message=message)

    def _get_room_name(self, sender_id, receiver_id):
        return 'chat_' + str(min(sender_id, receiver_id)) + '_' + str(max(sender_id, receiver_id))