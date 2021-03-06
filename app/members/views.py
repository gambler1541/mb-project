import imghdr

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile

from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, UserProfileForm

User = get_user_model()

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 인증 성공시
            login(request, form.user)
            # GET parameter에 'next'가 전달되었다면
            # 해당 키의 값으로 redirect
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post_list')
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'members/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('posts:post_list')

def signup_view(request):
    # render하는 경우
    #   1. POST요청이며, 사용자명이 이미 존재할 경우
    #   2. POST요청이며, 비밀번호가 같지 않은 경우
    #   3. GET요청인 경우
    # redirect하는 경우
    #   1. POST요청이며, 사용자명이 존재하지 않고 비밀번호가 같은 경우
    """
    if request.method가 POST면:
        if 사용자명이 존재하면:
            render
        if 비밀번호가 같지 않으면:
            render
        (else, POST면서 사용자도없고 비밀번호도 같으면):
            redirect
    (else, GET요청이면):
        render

    if request.method가 POST면:
        if 사용자명이 존재하면:
        if 비밀번호가 같지 않으면:
        (else, POST면서 사용자도없고 비밀번호도 같으면):
            redirect
    (else, GET요청이면):
        render


    :return:
    """
    context ={}
    if request.method == 'POST':
        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 post-list화면으로 이동
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('posts:post_list')
    # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
    #   signup.html에
    #       빈 Form또는 올바르지 않은 데이터에 대한 정보가 포함된 Form을 전달해서
    #       동적으로 form을 랜더
    else:
        form = SignupForm()
    context['form'] = form
    return render(request, 'members/signup.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user)
        context = {
            'form' : form
        }
    return render(request, 'members/profile.html', context)


def facebook_login(request):
    user = authenticate(request, facebook_request_token=request.GET.get('code'))
    if user:
        login(request, user)
        return redirect('posts:post_list')
    messages.error(request, '페이스북 로그인 실패')
    return redirect('members:login')
