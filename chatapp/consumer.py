from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
 
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer()
 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat%s' % self.room_name
 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
 
        await self.accept()
 
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )