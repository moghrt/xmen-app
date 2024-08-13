from rest_framework import serializers
from app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user_id = serializers.CharField(source='user.id', required=False)
    user_name = serializers.CharField(source='user.name', required=False)
    user_caption = serializers.CharField(source='user.caption', required=False)
    user_email = serializers.CharField(source='user.email', required=False)
    user_avatar_url = serializers.SerializerMethodField()

    def get_user_avatar_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        if obj.user.avatar:
            if request:
                return request.build_absolute_uri(obj.user.avatar.url)
            return obj.avatar.url
        return None

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'user',
            'post',
            'created_at',
            'user_id',
            'user_name',
            'user_caption',
            'user_email',
            'user_avatar_url',
        ]