from django.urls import re_path  # URL 패턴 매칭을 위한 함수

from . import consumers  # 현재 디렉토리의 consumers.py 파일 임포트

websocket_urlpatterns = [  # WebSocket URL 패턴 목록
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
    # WebSocket URL 패턴 정의:
    # - 'ws/chat/' 로 시작하는 URL
    # - '(?P<room_name>[^/]+)' : '/'를 제외한 모든 문자를 'room_name'이라는 그룹으로 캡처
    # - '/' 로 끝나는 URL
    # - 매칭되는 연결은 consumers.ChatConsumer.as_asgi() 로 처리
]