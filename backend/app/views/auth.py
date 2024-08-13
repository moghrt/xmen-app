
from rest_framework.authtoken.views import ObtainAuthToken

from app.serializers import  AuthTokenSerializer
    
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer