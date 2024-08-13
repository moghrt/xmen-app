from rest_framework import serializers
from app.models import Message

class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Message
        fields = [
            'id',
            'body',
            'sent_by',
            'created_at',
            'created_by',
            'room'
        ]