from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
            }
        )
    )

    def clean_username(self):
        # username이 유일한지 검사
        value = self.cleaned_data['username']
        if User.objects.filter(username=value).exists():
            raise forms.ValidationError('이미 있는 이름입니다.')
        return value

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('패스워드를 확인해 주세요.')
        return password2
    #
    # def clean(self):
    #     # password1, password2가 일치하는지 검사
    #     super().clean()
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('비밀번호를 확인하세요')