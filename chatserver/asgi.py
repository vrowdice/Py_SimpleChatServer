# chatserver/asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 이 부분이 Django 설정 파일을 정확히 가리키도록 합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatserver.settings')

# Django의 HTTP 및 일반적인 ASGI 애플리케이션을 로드합니다.
# 이 함수가 호출될 때 Django의 settings가 로드됩니다.
django_asgi_app = get_asgi_application()

# chat.routing 모듈은 django_asgi_app이 로드된 후에 임포트하는 것이 좋습니다.
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app, # 일반 HTTP 요청 처리
    "websocket": AuthMiddlewareStack( # WebSocket 요청 처리 (인증 미들웨어 스택 적용)
        URLRouter(
            chat.routing.websocket_urlpatterns # chat 앱의 WebSocket URL 패턴 사용
        )
    ),
})