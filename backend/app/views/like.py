from rest_framework import viewsets
from app.models import Like, User, Post
from app.serializers import LikeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class LikeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_context(self):
        context = super(LikeViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(methods=['post'], detail=False)
    def get_likes_by_user(self, request):
        user_id = request.data['user_id']
        queryset = Like.objects.filter(user__id=user_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    @action(methods=['post'], detail=False)
    def create_like(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
          
        newLike =  Like.objects.create(user=user, post=post)
        newLike.save()

        post.likes = post.likes + 1
        post.save()

        serializer = LikeSerializer(newLike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def destroy_like(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        post = Post.objects.get(id=post_id)

        likeItem = Like.objects.get(user__id=user_id, post__id=post_id)
        likeItem.delete()

        post.likes = post.likes - 1
        if(post.likes < 0):
            post.likes = 0
        post.save()

        serializer = LikeSerializer(likeItem)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)