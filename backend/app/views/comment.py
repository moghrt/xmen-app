from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models import Comment, Post, User
from app.serializers import CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    pagination_class= PageNumberPagination

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(methods=['post'], detail=False)
    def create_comment(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        comment = request.data['comment']

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
          
        newComment =  Comment.objects.create(user=user, post=post, text=comment)
        newComment.save()

        context = self.get_serializer_context()
        serializer = CommentSerializer(newComment, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
