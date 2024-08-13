from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers



class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request=self.context.get('request'), username = email, password = password)

        if not user:
            raise serializers.ValidationError('No se pudo autenticar', code= 'authorization')
        
        data['user'] = user
        
        return data
