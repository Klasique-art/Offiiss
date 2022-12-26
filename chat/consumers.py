from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json

class Chat(WebsocketConsumer):
    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['code']
        sync_to_async(self.channel_layer.group_add)(self.chat_name, self.channel_name)
        self.accept()
    def disconnect(self, close_code):
        sync_to_async(self.channel_layer.group_discard)(self.chat_name, self.channel_name)
    def recieve(self, text_data):
        text = json.loads(text_data['message'])
        sync_to_async(self.channel_layer.group_send)(self.chat_name, {"type": "chat_message", "message": text})
    def chat_message(self, event):
        message = json.loads(event['mesage'])
        self.send(text_data={"message": message})
