from rest_framework import viewsets
from app.models import Room
from app.serializers import RoomSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RoomViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all().order_by('created_at')
    serializer_class = RoomSerializer

    def get_serializer_context(self):
        context = super(RoomViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context
    
'''@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})'''