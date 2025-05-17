import os  # OS 관련 기능
from channels.auth import AuthMiddlewareStack  # WebSocket 인증 처리
from channels.routing import ProtocolTypeRouter, URLRouter  # 프로토콜 기반 라우팅, URL 기반 라우팅
from django.core.asgi import get_asgi_application  # Django ASGI 앱 가져오기
import chat.routing  # 'chat' 앱의 라우팅 설정

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatserver.settings')  # Django 설정 로드

application = ProtocolTypeRouter({  # ASGI 최상위 라우터
    "http": get_asgi_application(),  # HTTP 요청 처리 (Django)
    "websocket": AuthMiddlewareStack(  # WebSocket 요청 처리 (인증 추가)
        URLRouter(  # WebSocket URL 라우팅
            chat.routing.websocket_urlpatterns  # 'chat' 앱의 WebSocket URL 패턴
        )
    ),
})