from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from app.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from app.helpers.pagination_extras import UsersNumberPagination
from django.db.models import Q
from django.core.paginator import Paginator
from app.models import User
from django.conf import settings

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = UsersNumberPagination
    #pagination_class=PageNumberPagination


    @action(methods=['post'], detail=False)
    def get_users(self, request):
        if 'filter_by_user' in request.data:
            user_id = request.data['user_id']
            queryset = User.objects.filter(Q(user__id=user_id), ~Q(user__type='ADMIN')).order_by('name')
        else:
            queryset = User.objects.filter(~Q(user_type='ADMIN')).order_by('name')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=False)
    def get_users_paginated(self, request):
        if 'filter_by_user' in request.data:
            user_id = request.data['user_id']
            queryset = User.objects.filter(user__id=user_id).order_by('name')
        else:
            queryset = User.objects.all().order_by('name')

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super(UserView, self).get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        context = self.get_serializer_context()   
        serializer = UserSerializer(user, context=context)
        return Response(serializer.data)

class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user