import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationsConsumer(WebsocketConsumer):
    def connect(self):

        user_id = self.scope['url_route']['kwargs']['userId']

        self.room_group_name = f'notifications_{user_id}'

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

    def send_notification(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))


class SummonerConsumer(WebsocketConsumer):
    def connect(self):

        server = self.scope['url_route']['kwargs']['server']
        summoner_id = self.scope['url_route']['kwargs']['summonerId']

        self.room_group_name = f'summoner-{server}-{summoner_id}'

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

    def send_match(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))

