"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import routers
from app import views
from app import consumers
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet),
router.register(r'likes', views.LikeViewSet),
router.register(r'comments', views.CommentViewSet),
router.register(r'users', views.UserView),
router.register(r'rooms', views.RoomViewSet),

# Chat URLs
websocket_urlpatterns = [
    #path(r"api/v1/ws/chatroom/<str:chatroom_name>", consumers.ChatroomConsumer.as_asgi() ),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatroomConsumer.as_asgi()),  
]

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'api/v1/token/create/', views.CreateTokenView.as_view()),
    path(r'api/v1/user/create/', views.CreateUserView.as_view()),
    path(r'api/v1/user/', views.UserMeView.as_view()),
    path(r'api/v1/', include('djoser.urls')),
    path(r'api/v1/', include('djoser.urls.jwt')),
    #path(r"api/v1/room/create/<str:uuid>/", views.create_room, name="create-room"),
    #path(r"api/v1/prueba-chat/", views.index, name="index"),
    path(r"api/v1/prueba-chat/<str:room_name>/", views.chat_room, name="room"),

    #path(r"api/v1/ws/chatroom/<str:chatroom_name>", consumers.ChatroomConsumer.as_asgi())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
