#forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ChatRoom

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="아이디", widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '새로운 방 이름'}),
        }
