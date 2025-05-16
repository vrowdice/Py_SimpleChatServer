# chat/urls.py
from django.urls import path
from .views import home, chatroom, register, login_view, logout_view, create_room, room_list, delete_room

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('rooms/', room_list, name='room_list'),
    path('chatroom/<str:room_name>/', chatroom, name='chatroom'),
    path('chatroom/<str:room_name>/delete/', delete_room, name='delete_room'), # 삭제 URL
    path('logout/', logout_view, name='logout'),
    path('create_room/', create_room, name='create_room'),
]