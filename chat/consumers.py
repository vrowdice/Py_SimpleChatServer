# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, Message

# 각 채팅방별 온라인 사용자들을 저장할 딕셔너리
# 실제 운영 환경에서는 Redis 등의 외부 저장소를 사용해야 합니다.
# 개발 및 테스트를 위해 일단 파이썬 딕셔너리를 사용합니다.
online_users_by_room = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            # 로그인되지 않은 사용자는 연결 거부
            await self.close(code=4001) # 4001은 사용자 정의 코드 (Unauthorized)
            return

        # 방 그룹에 조인
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # 사용자 목록 업데이트 및 전송
        await self.add_user_to_room()
        await self.send_online_users_to_room()

    async def disconnect(self, close_code):
        if not self.user.is_authenticated:
            return

        # 방 그룹에서 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # 사용자 목록에서 제거 및 전송
        await self.remove_user_from_room()
        await self.send_online_users_to_room()

        print(f"WebSocket disconnected with code: {close_code}")
        print(f"Current online users for room {self.room_name}: {online_users_by_room.get(self.room_name, set())}")

    # WebSocket으로부터 메시지 수신
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.user.username

        # 메시지를 방 그룹으로 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        # 메시지를 DB에 저장
        await self.save_message(username, message)

    # 방 그룹으로부터 메시지 수신 (실제 클라이언트에 전송)
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # WebSocket으로 메시지 전송
        await self.send(text_data=json.dumps({
            'type': 'chat_message', # 메시지 타입 추가
            'message': message,
            'username': username
        }))

    # 온라인 사용자 목록 업데이트 메시지 수신 (실제 클라이언트에 전송)
    async def online_users_message(self, event):
        online_users = event['online_users']
        await self.send(text_data=json.dumps({
            'type': 'online_users_update', # 메시지 타입 추가
            'online_users': online_users
        }))

    # DB에 메시지 저장 (비동기 처리)
    @sync_to_async
    def save_message(self, username, message_content):
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=user, content=message_content)

    # 방에 사용자 추가
    async def add_user_to_room(self):
        user_id = str(self.user.id) # 사용자를 고유하게 식별할 ID 사용
        if self.room_name not in online_users_by_room:
            online_users_by_room[self.room_name] = set()
        online_users_by_room[self.room_name].add(user_id) # ID를 저장

    # 방에서 사용자 제거
    async def remove_user_from_room(self):
        user_id = str(self.user.id)
        if self.room_name in online_users_by_room:
            online_users_by_room[self.room_name].discard(user_id) # ID를 제거
            if not online_users_by_room[self.room_name]: # 방에 남은 사용자가 없으면 방 엔트리 삭제
                del online_users_by_room[self.room_name]

    # 현재 방의 온라인 사용자 목록을 모든 클라이언트에게 전송
    async def send_online_users_to_room(self):
        if self.room_name in online_users_by_room:
            # 온라인 사용자 ID 목록을 실제 username으로 변환
            user_ids = list(online_users_by_room[self.room_name])
            usernames = await self.get_usernames_from_ids(user_ids)
            online_user_list = sorted(list(usernames)) # 정렬하여 전송

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_users_message',
                    'online_users': online_user_list,
                }
            )

    @sync_to_async
    def get_usernames_from_ids(self, user_ids):
        # User 모델을 통해 ID로 사용자 이름을 가져옵니다.
        return list(User.objects.filter(id__in=user_ids).values_list('username', flat=True))