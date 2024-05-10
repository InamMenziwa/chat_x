from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import messages, ChatRoom
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
 
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer()
 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat%s' % self.room_name
 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
 
        await self.accept()
 
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user = data["user_name"]
        room = data["room"]
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type":"chat_message",
                "message":message,
                "user":user,
                "room":room,
            }
        )
        await self.save_message(user,room, message)
        
    async def chat_message(self, event):
        messsage = event["message"]
        user_name = event["user"]
        room = event["room"]
        
        await self.send(text_data=json.dumps({
            "message":messsage,
            "user_name":user_name,
            "room":room,
        }))
        
    @sync_to_async
    def save_message(self, user, room, message):
        user = User.objects.get(username=user)
        room = ChatRoom.objects.get(slug=room)
        messages.objects.create(user=user, room=room, message_content=message)
        