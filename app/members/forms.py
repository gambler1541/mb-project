from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 이 Form instance에 주어진 데이터가 유효하면
        # authenticate에서 리턴된 User객체를 채울 속성
        self._user = None

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

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username = username, password = password)
        if user is None:
            raise forms.ValidationError('로그인 정보를 확인하세요.')
        self._user = user

    @property
    def user(self):
        # 유효성 검증을 실행했을 때(is_valid())
        #  만약 필드나 폼에서 유효하지 않은 항목이 있다면
        #  이 부분에 추가됨
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였습니다.')
        return self._user

class SignupForm(forms.Form):
    username = forms.CharField(
        label='사용자명',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
            }
        )
    )

    img_profile = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class':'form-control-file',
            }
        )
    )


    def clean_username(self):
        # username이 유일한지 검사
        value = self.cleaned_data['username']
        if User.objects.filter(username=value).exists():
            self.fields['username'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('이미 있는 이름입니다.')
        return value

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            self.fields['password1'].widget.attrs['class'] += ' is-invalid'
            self.fields['password2'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('패스워드를 확인해 주세요.')
        return password2

    def save(self):
        if self.errors:
            raise ValueError('데이터 유효성 검증에 실패했습니다.')
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password2'],
            img_profile=self.cleaned_data['img_profile'],
        )
        return user
    #
    # def clean(self):
    #     # password1, password2가 일치하는지 검사
    #     super().clean()
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('비밀번호를 확인하세요')