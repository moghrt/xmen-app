from rest_framework import serializers
from app.models import Post, User, Like, Comment
from app.serializers.user import UserSerializer
from app.serializers.comment import CommentSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.conf import settings

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    likes = serializers.IntegerField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #user_data = serializers.SerializerMethodField()
    user_id = serializers.CharField(source='user.id', required=False)
    user_name = serializers.CharField(source='user.name', required=False)
    user_caption = serializers.CharField(source='user.caption', required=False)
    user_email = serializers.CharField(source='user.email', required=False)
    user_avatar_url = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()

    def get_number_of_comments(self, obj):
        comments = Comment.objects.filter(post__id=obj.id).count()
        return comments
    
    def get_user_data(self, obj):
        serializer = UserSerializer(User.objects.filter(id=obj.user_id), many=True, context=self.context)
        return serializer.data
    
    def get_user_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.user.avatar:
            if request:
                return request.build_absolute_uri(obj.user.avatar.url)
            return obj.avatar.url
        return None
    def get_liked_by_me(self, obj, pk=None):
        request = self.context.get('request')
        front_end_user_id = None
        for key, value in request.data.items():
            if 'user_id' in key:
                front_end_user_id = value
        if front_end_user_id is None:
            return False
        try:    
            Like.objects.get(user__id=front_end_user_id, post__id=obj.pk)
            return True
        except Like.DoesNotExist:
            return False
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'user',
            'image',
            'likes',
            'created_at',
            'liked_by_me',
            #'user_data',
            'user_id',
            'user_name',
            'user_caption',
            'user_email',
            'user_avatar_url',
            'number_of_comments',
        ]


class PostSerializerComments(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    likes = serializers.IntegerField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    liked_by_me = serializers.SerializerMethodField()
    #user_data = serializers.SerializerMethodField()
    user_id = serializers.CharField(source='user.id', required=False)
    user_name = serializers.CharField(source='user.name', required=False)
    user_caption = serializers.CharField(source='user.caption', required=False)
    user_email = serializers.CharField(source='user.email', required=False)
    user_avatar_url = serializers.SerializerMethodField()
    comments =  serializers.SerializerMethodField()
    comments_total = serializers.SerializerMethodField()

    def get_comments_total(self, obj):
        total = Comment.objects.filter(post__id=obj.id).count()
        return total
    
    def get_comments(self, obj):
        queryset = Comment.objects.filter(post__id=obj.id).order_by('created_at')
        # Uso el paginador de django.
        # el número de la página que quiero sacar, viene desde el contexto del request de la vista.
        page_number = self.context.get('request').data.get('page')
        if page_number:
            # Tamaño de la página, desde los settings.
            page_size = settings.REST_FRAMEWORK['COMMENTS_PER_PAGE']
            # Pagino el queryset.
            paginator = Paginator(queryset, page_size)
            # Devuelvo la página serializada que me interesa.
            page = paginator.page(page_number)
            serializer = CommentSerializer(page, many=True, context=self.context)
        else:
            serializer = CommentSerializer(queryset, many=True, context=self.context)
        return serializer.data

    def get_user_data(self, obj):
        serializer = UserSerializer(User.objects.filter(id=obj.user_id), many=True, context=self.context)
        return serializer.data
    
    def get_user_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.user.avatar:
            if request:
                return request.build_absolute_uri(obj.user.avatar.url)
            return obj.avatar.url
        return None
    
    def get_liked_by_me(self, obj, pk=None):
        request = self.context.get('request')
        front_end_user_id = None
        for key, value in request.data.items():
            if 'user_id' in key:
                front_end_user_id = value
        if front_end_user_id is None:
            return False
        try:    
            Like.objects.get(user__id=front_end_user_id, post__id=obj.pk)
            return True
        except Like.DoesNotExist:
            return False
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'user',
            'image',
            'likes',
            'liked_by_me',
            'comments',
            'comments_total',
            'created_at',
            #'user_data',
            'user_id',
            'user_name',
            'user_caption',
            'user_email',
            'user_avatar_url'
        ]