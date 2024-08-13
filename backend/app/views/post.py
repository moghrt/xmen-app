from rest_framework import viewsets, authentication, permissions
from app.models import Post
from app.serializers import PostSerializer, PostSerializerComments
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class=PageNumberPagination

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(methods=['post'], detail=False)
    def get_posts(self, request):
        if 'filter_by_user' in request.data:
            user_id = request.data['user_id']
            queryset = Post.objects.filter(user__id=user_id).order_by('-created_at')
        else:
            queryset = Post.objects.all().order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=False)
    def detail_post(self, request):
        post_id = request.data['post_id']

        queryset = Post.objects.get(id=post_id)   
         
        context = self.get_serializer_context()    
        serializer = PostSerializerComments(queryset, context=context)
        return Response(serializer.data)
    
