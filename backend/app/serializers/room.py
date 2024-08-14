from rest_framework import serializers
from app.models import Room, Message
from app.serializers.message import MessageSerializer

class RoomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    messages = MessageSerializer(many=True)

    def get_user_avatar_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        if obj.author.avatar:
            if request:
                return request.build_absolute_uri(obj.author.avatar.url)
            return obj.avatar.url
        return None

    class Meta:
        model = Room
        fields = [
            'id',
            'uuid',
            'name',
            'caption',
            'image',
            'author',
            'created_at',
            'type',
            'messages',
            'tags',
        ]