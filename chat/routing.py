# chat/routing.py

from django.urls import re_path

from . import consumers # chat 앱의 consumers.py 임포트

websocket_urlpatterns = [
    # room_name은 /를 포함할 수 없으므로, [^/]+ 를 사용합니다.
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]