# colis/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LivreurTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.livraison_id = self.scope['url_route']['kwargs']['livraison_id']
        self.room_group_name = f'livraison_{self.livraison_id}'

        # Rejoindre le groupe de la livraison
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de la livraison
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Optionnel : Gérer les messages reçus du client
        data = json.loads(text_data)
        print(f"Received data: {data}")

    async def send_position(self, event):
        # Envoyer la position au client
        await self.send(text_data=json.dumps({
            'position': event['position']
        }))
