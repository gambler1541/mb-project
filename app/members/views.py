import imghdr
import io
import json

import requests
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile

from django.http import HttpResponse
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
    # request token
    api_base = 'https://graph.facebook.com/v3.2/'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'
    code = request.GET['code']
    params  = {
        'client_id': '2270191476551895',
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        # 'client_secret': {secret}
        'code': code

    }
    # request token을 access token으로 교환
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 `JSON`형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON일 경우, 해당 문자열을 parsing해서 python 객체로 변환
    data = response.json()
    access_token = data['access_token']
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'name',
            # 프로필 사진을 원본크기로
            'picture.type(large)',
        ])
    }
    # access_token을 이용해 data를 받음
    response = request.get(api_me, params)
    data = response.json()

    # api_me로 get요청을 보내 받은 response의 data
    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']
    # 이미지 url로 get요청을 보내 img를 가져옴
    img_response = request.get(url_img_profile)
    # FileField가 지원하는 InMemoryUploadedFile객체 사용
    img_data = img_response.content
    # 확장자를 가져오기 위한 패키지
    ext = imghdr.what('', h=img_data)
    # Form에서 업로드한 것과 같은 형태의 file-like object생성
    #  첫 번째 인수로 반드시 파일명이 필요. <facebook_id>.<확장자>형태의 파일명을 지
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

    try:
        user = User.objects.get(username=facebook_id)
        # update_or_create
        # facebook_id를 제외한 모든 필드는 facebook에서 수정될 때마다 갱신
        user.last_name = last_name
        user.first_name = first_name
        user.img_profile = f
        user.seve()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
            img_profile=f,
        )
    login(request, user)

    return redirect('posts:post_list')
