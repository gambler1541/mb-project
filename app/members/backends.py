from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

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