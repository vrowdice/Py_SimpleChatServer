# chat/models.py

from django.db import models
from django.contrib.auth.models import User # Django의 User 모델 임포트

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) # 생성 시간 필드 추가 (권장)

    def __str__(self):
        return self.name

class Message(models.Model): # <--- 이 Message 모델 정의를 추가해야 합니다.
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 메시지를 보낸 사용자
    content = models.TextField() # 메시지 내용
    timestamp = models.DateTimeField(auto_now_add=True) # 메시지 전송 시간

    class Meta:
        ordering = ['timestamp'] # 메시지를 오래된 것부터 최신 순으로 정렬

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}' # 관리자 페이지 등에서 보기 좋게