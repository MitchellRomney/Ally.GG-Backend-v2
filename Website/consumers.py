import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SummonerConsumer(WebsocketConsumer):
    def connect(self):

        summoner_id = self.scope['url_route']['kwargs']['summonerId']
        server = self.scope['url_route']['kwargs']['server']

        self.room_group_name = f'summoner_{server}_{summoner_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def celery(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))
