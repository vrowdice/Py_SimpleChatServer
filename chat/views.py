# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # User 모델 임포트 추가
from django.contrib import messages
from .forms import RegisterForm, CreateRoomForm
from .models import ChatRoom

# ---
## 기본 페이지 (로그인 여부에 따라 리다이렉션)
def home(request):
    # 사용자가 이미 로그인되어 있다면, 채팅방 목록으로 바로 리다이렉트
    if request.user.is_authenticated:
        return redirect('room_list')
    # 로그인되어 있지 않다면, 로그인/회원가입을 위한 홈 페이지 렌더링
    return render(request, 'chat/home.html')

# ---
## 로그인 처리
def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('room_list')  # 로그인 성공 시 채팅방 목록으로 이동
        else:
            error_message = '아이디 또는 비밀번호가 올바르지 않습니다.'
            # 인증 실패 시 에러 메시지와 함께 홈 페이지 다시 렌더링
            return render(request, 'chat/home.html', {'error': error_message})
    # GET 요청이거나 인증 실패 시 홈 페이지 렌더링 (에러 메시지 포함)
    return render(request, 'chat/home.html', {'error': error_message})

# ---
## 회원가입 처리
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 성공적으로 완료되었습니다. 로그인해주세요.')
            return redirect('home')  # 회원가입 성공 시 홈 페이지로 리다이렉트
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {'form': form})

# ---
## 로그아웃 처리
def logout_view(request):
    logout(request)
    messages.info(request, '로그아웃 되었습니다.')
    return redirect('home')  # 로그아웃 후 홈 페이지로 리다이렉트

# ---
## 채팅방 목록 및 생성 페이지
@login_required
def room_list(request):
    rooms = ChatRoom.objects.all()
    form = CreateRoomForm()
    # 모든 등록된 사용자 목록을 가져옵니다.
    # 본인(request.user)을 제외하려면 .exclude(id=request.user.id) 추가
    all_users = User.objects.all().order_by('username')

    context = {
        'rooms': rooms,
        'form': form,
        'users': all_users, # 템플릿에 사용자 목록 전달
    }
    return render(request, 'chat/rooms.html', context)

# ---
## 새로운 채팅방 생성
@login_required
def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'"{room.name}" 채팅방이 생성되었습니다.')
            return redirect('chatroom', room_name=room.name)
    messages.error(request, '채팅방 생성에 실패했습니다.')
    return redirect('room_list') # 생성 실패 시 목록 페이지로 리다이렉트

# ---
## 특정 채팅방 입장
@login_required
def chatroom(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    context = {
        'room_name': room.name,
        'username': request.user.username # 현재 사용자 이름
    }
    return render(request, 'chat/chatroom.html', context)

# ---
## 채팅방 삭제
@login_required
def delete_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    if request.method == 'POST':
        room.delete()
        messages.success(request, f'"{room.name}" 채팅방이 삭제되었습니다.')
        return redirect('room_list')
    else:
        messages.error(request, '잘못된 접근입니다.')
        return redirect('chatroom', room_name=room_name) # POST 요청이 아니면 해당 채팅방으로 다시 이동