from rest_framework import viewsets
from app.models import Room, User
from app.serializers import RoomSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse


class RoomViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all().order_by('created_at')
    serializer_class = RoomSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super(RoomViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(methods=['post'], detail=False)
    def create_room(self, request):
        if len(request.data) > 0:
            author_id = request.data['authorId']
            author = User.objects.get(id=author_id)
            author_name = request.data['authorName']
            requestImage = request.data['image']
            uuid = str(author_id) + '-'
            name = ''
            items = request.data['items']
            image = 'avatars' + requestImage.split('avatars', 1)[1]
            for item in items:
                item_id = item.get('id', '')
                item_name = item.get('name', '')
                uuid += str(item_id) + '-'
                name += item_name + ', '

            name += author_name
            uuid = uuid[:-1]
            Room.objects.create(uuid=uuid, name=name, image=image, caption='', author=author)

            return JsonResponse({'message': 'room created.'})      
        return JsonResponse({'message': 'Can´t create room.'})