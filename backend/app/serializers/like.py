from rest_framework import serializers
from app.models import Like, Post, User
from app.serializers.user import UserSerializer

class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Like
        fields = [
            'id',
            'post',
            'user',
        ]