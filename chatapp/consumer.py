from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
 
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
 
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        messsage = data["message"]
        user = data["user_name"]
        room = data["room"]
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type":"chat_message",
                "message":messsage,
                "user":user,
                "room":room,
            }
        )
        
    async def chat_message(self, event):
        messsage = event["message"]
        user_name = event["user"]
        room = event["room"]
        
        await self.send(text_data=json.dumps({
            "message":messsage,
            "user_name":user_name,
            "room":room,
        }))