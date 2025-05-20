from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from captcha.fields import CaptchaField

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")
