from django.shortcuts import render, redirect, get_object_or_404  # 렌더링, 리다이렉트, 객체 찾기 또는 404 에러
from django.contrib.auth import authenticate, login, logout  # 사용자 인증, 로그인, 로그아웃
from django.contrib.auth.decorators import login_required  # 로그인Required 데코레이터
from .forms import RegisterForm  # RegisterForm 임포트
from .models import ChatRoom  # ChatRoom 모델 임포트
from .forms import CreateRoomForm  # CreateRoomForm 임포트
from django.contrib import messages  # 메시지 프레임워크

def home(request):
    return render(request, 'chat/home.html')  # 홈페이지 렌더링

def login_view(request):
    error_message = None  # 에러 메시지 초기화
    if request.method == 'POST':  # POST 요청 처리
        username = request.POST.get('username')  # 폼에서 아이디 가져오기
        password = request.POST.get('password')  # 폼에서 비밀번호 가져오기
        user = authenticate(request, username=username, password=password)  # 사용자 인증
        if user:  # 인증 성공
            login(request, user)  # 사용자 로그인
            return redirect('room_list')  # 채팅방 목록 페이지로 리다이렉트
        else:  # 인증 실패
            error_message = '아이디 또는 비밀번호가 올바르지 않습니다.'  # 에러 메시지 설정
            return render(request, 'chat/home.html', {'error': error_message})  # 에러 메시지와 함께 홈페이지 렌더링
    return render(request, 'chat/home.html', {'error': error_message})  # GET 요청 시 또는 인증 실패 후 에러 메시지와 함께 홈페이지 렌더링

def register(request):
    if request.method == 'POST':  # POST 요청 처리
        form = RegisterForm(request.POST)  # 폼 생성 및 데이터 바인딩
        if form.is_valid():  # 폼 유효성 검사
            form.save()  # 사용자 저장
            return redirect('home')  # 홈페이지로 리다이렉트
    else:  # GET 요청 처리
        form = RegisterForm()  # 빈 폼 생성
    return render(request, 'chat/register.html', {'form': form})  # 회원가입 폼 렌더링

@login_required  # 로그인된 사용자만 접근 가능
def home(request):  # 중복된 데코레이터 제거
    rooms = ChatRoom.objects.all()  # 모든 채팅방 목록 가져오기
    form = CreateRoomForm()  # 채팅방 생성 폼 생성
    context = {'rooms': rooms, 'form': form}  # 템플릿에 전달할 컨텍스트
    return render(request, 'chat/home.html', context)  # 채팅방 목록 및 생성 폼 렌더링

@login_required  # 로그인된 사용자만 접근 가능
def create_room(request):
    if request.method == 'POST':  # POST 요청 처리
        form = CreateRoomForm(request.POST)  # 폼 생성 및 데이터 바인딩
        if form.is_valid():  # 폼 유효성 검사
            room = form.save()  # 채팅방 저장
            return redirect('chatroom', room_name=room.name)  # 해당 채팅방 페이지로 리다이렉트
    return redirect('home')  # POST 요청이 아니면 홈페이지로 리다이렉트

@login_required  # 로그인된 사용자만 접근 가능
def chatroom(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)  # 주어진 이름의 채팅방 가져오기, 없으면 404 에러
    context = {
        'room_name': room.name,  # 채팅방 이름
        'username': request.user.username  # 현재 사용자 이름
    }
    return render(request, 'chat/chatroom.html', context)  # 채팅방 페이지 렌더링

@login_required  # 로그인된 사용자만 접근 가능
def delete_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)  # 주어진 이름의 채팅방 가져오기, 없으면 404 에러
    if request.method == 'POST':  # POST 요청 처리 (삭제 요청)
        room.delete()  # 채팅방 삭제
        messages.success(request, f'"{room.name}" 채팅방이 삭제되었습니다.')  # 성공 메시지 표시
        return redirect('room_list')  # 채팅방 목록 페이지로 리다이렉트
    else:  # POST 요청이 아닌 경우
        messages.error(request, '잘못된 접근입니다.')  # 에러 메시지 표시
        return redirect('chatroom', room_name=room_name)  # 해당 채팅방 페이지로 리다이렉트

@login_required  # 로그인된 사용자만 접근 가능
def room_list(request):
    rooms = ChatRoom.objects.all()  # 모든 채팅방 목록 가져오기
    form = CreateRoomForm()  # 채팅방 생성 폼 생성
    context = {'rooms': rooms, 'form': form}  # 템플릿에 전달할 컨텍스트
    return render(request, 'chat/rooms.html', context)  # 채팅방 목록 페이지 렌더링

def logout_view(request):
    logout(request)  # 사용자 로그아웃
    return redirect('home')  # 홈페이지로 리다이렉트