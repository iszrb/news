from django import forms
from captcha.fields import CaptchaField
from app.models import *

class SignupForm(forms.ModelForm):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

    class Meta:
        model = UserInfo
        fields = ["username", "password","email", "mobile", "gender"]
        error_messages = {
            "username": {"invalid": "用户名错误"},
            "password": {"invalid": "密码错误"},
        } 

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['gender', 'mobile','image', 'email']

class PasswordForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    re_password = forms.CharField(required=True, min_length=5)

class ForGetPasswordForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"}, label="验证码")
    username = forms.CharField(max_length=30)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
