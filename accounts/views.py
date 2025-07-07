from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages  # ✅ 추가

User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        
        user = User.objects.create(
            username=username,
            password=make_password(raw_password)
        )
        messages.success(request, '✅ 회원가입이 완료되었습니다. 로그인해주세요.')
        return redirect('login')
    return render(request, 'blog/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        
        user = authenticate(request, username=username, password=raw_password)
        if user is not None:
            login(request, user)
            messages.success(request, f'🎉 {user.username}님, 환영합니다!')
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'error': '로그인 실패'})
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, '👋 로그아웃되었습니다.')
    return redirect('/')


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ 프로필이 성공적으로 수정되었습니다.')
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('edit_profile')

    def form_valid(self, form):
        messages.success(self.request, '🔐 비밀번호가 성공적으로 변경되었습니다.')
        return super().form_valid(form)
