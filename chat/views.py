from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import ChatRoom
from .forms import CreateRoomForm
from django.contrib import messages

def home(request):
    return render(request, 'chat/home.html')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('room_list') # 채팅방 목록 페이지로 리다이렉트
        else:
            error_message = '아이디 또는 비밀번호가 올바르지 않습니다.'
            return render(request, 'chat/home.html', {'error': error_message})
    return render(request, 'chat/home.html', {'error': error_message})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def home(request): # 중복된 데코레이터 제거
    rooms = ChatRoom.objects.all()
    form = CreateRoomForm()
    context = {'rooms': rooms, 'form': form}
    return render(request, 'chat/home.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('chatroom', room_name=room.name)
    return redirect('home')

@login_required
def chatroom(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    context = {
        'room_name': room.name,
        'username': request.user.username
    }
    return render(request, 'chat/chatroom.html', context)

@login_required
def delete_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    if request.method == 'POST':
        room.delete()
        messages.success(request, f'"{room.name}" 채팅방이 삭제되었습니다.')
        return redirect('room_list')
    else:
        messages.error(request, '잘못된 접근입니다.')
        return redirect('chatroom', room_name=room_name)

@login_required
def room_list(request):
    rooms = ChatRoom.objects.all()
    form = CreateRoomForm()
    context = {'rooms': rooms, 'form': form}
    return render(request, 'chat/rooms.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')