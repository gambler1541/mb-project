import imghdr

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class SettingsBackend:
    def authenticate(self, request, username=None, password=None):
        # 가독성을 위해 괄호(())를 붙임
        login_valid = (settings.ADMIN_LOGIN == username)
        password_valid = check_password(password, settings.ADMIN_PASSWORD)

        if login_valid and password_valid:
            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        # request token
        api_base = 'https://graph.facebook.com/v3.2/'
        api_get_access_token = f'{api_base}/oauth/access_token'
        api_me = f'{api_base}/me'
        code = request.GET['code']
        params = {
            'client_id': settings.base.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.base.FACEBOOK_APP_SECRET,
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
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None