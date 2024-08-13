from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.models import Post


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    avatar_url = serializers.SerializerMethodField() 
    number_of_posts = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields=[
            'id',
            'email',
            'password',
            'name',
            'avatar_url',
            'caption',
            'number_of_posts',
            'tags',
        ]
        extra_kwargs = {'password' : {'write_only': True}}

    def get_number_of_posts(self, obj):
        result = Post.objects.filter(user__id=obj.id).count()
        return result
    
    def get_avatar_url(self, obj):
        if not bool(obj.avatar):
            return
        
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url

    def create(self, validate_data):
        return get_user_model().objects.create_user(**validate_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user=super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user