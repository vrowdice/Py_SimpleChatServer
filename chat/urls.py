# chat/urls.py
from django.urls import path  # URL 패턴 정의를 위한 함수
from .views import home, chatroom, register, login_view, logout_view, create_room, room_list, delete_room
# 현재 디렉토리의 views.py 파일에서 필요한 뷰 함수들을 임포트합니다.

urlpatterns = [
    path('', home, name='home'),  # 루트 URL ('/') 에 대해 home 뷰 함수를 연결하고, 'home'이라는 이름으로 URL 패턴을 정의합니다.
    path('login/', login_view, name='login'),  # '/login/' URL에 대해 login_view 뷰 함수를 연결하고, 'login'이라는 이름으로 URL 패턴을 정의합니다.
    path('register/', register, name='register'),  # '/register/' URL에 대해 register 뷰 함수를 연결하고, 'register'이라는 이름으로 URL 패턴을 정의합니다.
    path('rooms/', room_list, name='room_list'),  # '/rooms/' URL에 대해 room_list 뷰 함수를 연결하고, 'room_list'이라는 이름으로 URL 패턴을 정의합니다. (채팅방 목록)
    path('chatroom/<str:room_name>/', chatroom, name='chatroom'),
    # '/chatroom/<str:room_name>/' URL에 대해 chatroom 뷰 함수를 연결하고, 'chatroom'이라는 이름으로 URL 패턴을 정의합니다.
    # <str:room_name>은 URL 경로의 변수 부분으로, 문자열 형태의 'room_name'을 뷰 함수에 전달합니다.
    path('chatroom/<str:room_name>/delete/', delete_room, name='delete_room'),  # 삭제 URL
    # '/chatroom/<str:room_name>/delete/' URL에 대해 delete_room 뷰 함수를 연결하고, 'delete_room'이라는 이름으로 URL 패턴을 정의합니다.
    # 특정 채팅방 삭제를 위한 URL 패턴입니다.
    path('logout/', logout_view, name='logout'),  # '/logout/' URL에 대해 logout_view 뷰 함수를 연결하고, 'logout'이라는 이름으로 URL 패턴을 정의합니다.
    path('create_room/', create_room, name='create_room'),  # '/create_room/' URL에 대해 create_room 뷰 함수를 연결하고, 'create_room'이라는 이름으로 URL 패턴을 정의합니다. (채팅방 생성)
]