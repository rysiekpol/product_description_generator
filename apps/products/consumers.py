import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProductDescriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = (
            f"product_{self.scope['url_route']['kwargs']['product_id']}"
        )
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def description_update(self, event):
        print("test description update")
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
