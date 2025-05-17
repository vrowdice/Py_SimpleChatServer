# forms.py
from django import forms  # Django 폼 관련 모듈
from django.contrib.auth.forms import UserCreationForm  # 사용자 생성 폼
from django.contrib.auth.models import User  # Django 사용자 모델
from .models import ChatRoom  # 현재 디렉토리의 models.py에서 ChatRoom 모델 임포트

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username'}))  # 사용자 아이디 필드
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))  # 비밀번호 필드
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))  # 비밀번호 확인 필드

    class Meta:
        model = User  # 사용할 모델은 Django의 User 모델
        fields = ['username', 'password1', 'password2']  # 폼에 포함할 필드 목록

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom  # 사용할 모델은 ChatRoom 모델
        fields = ['name']  # 폼에 포함할 필드는 'name'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'New Room Name'}),  # 'name' 필드의 위젯 설정 (텍스트 입력, placeholder 설정)
        }