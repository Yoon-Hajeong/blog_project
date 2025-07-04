from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        
        # 비밀번호 암호화
        user = User.objects.create(
            username=username,
            password=make_password(raw_password)
        )
        return redirect('login')  # 회원가입 후 로그인 페이지로
    return render(request, 'blog/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        
        user = authenticate(request, username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return redirect('/')  # 로그인 성공 시 메인으로
        else:
            return render(request, 'blog/login.html', {'error': '로그인 실패'})
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')