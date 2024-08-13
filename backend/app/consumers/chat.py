from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.utils.timesince import timesince
from app.models import Message, Room, User
from asgiref.sync import sync_to_async
from app.helpers.chat_extras import initials
import json

class ChatroomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Unirse al grupo /room.
        #await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        #Dejar el grupo.
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def send_message(self, event):
        '''message = event["message"]

        #Enviar mensage por websocket.
        self.send(text_data=json.dumps({"message": message}))'''
        pass

    # Recibe mensaje del WEbSocket (frontend).
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        author = text_data_json.get("author", '')
        sent_by = text_data_json.get("sent_by", '')
        type = text_data_json["type"]

        if type == 'message':
            # Salvamos el mensage en la BBDD.
            new_message = await self.create_message(sent_by, body)
            
            # Enviamos el mensaje al grupo / room.
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "body": body,
                    'sent_by': sent_by,
                    'initials': initials(sent_by),
                    'created_at': '',#timesince(new_message.created_at),
            })

    # Mensaje recibido del grupo / room.
    async def chat_message(self, event):
        body = event["body"]
        sent_by = event["sent_by"]
        initials = event["initials"]
        created_at = event["created_at"]

        # Envía el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            "body": body,
            "sent_by": sent_by,
            "initials": initials,
            "created_at": created_at,
        }))

    @sync_to_async
    def create_message(self, sent_by, message):
        message = Message.objects.create(body=message,room_id = self.room_name, sent_by=sent_by)

        if sent_by:
            message.created_by = User.objects.get(name=sent_by)
            message.save()

        #self.room.messages.add(message)