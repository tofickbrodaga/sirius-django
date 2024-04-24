from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from rest_framework.authtoken.models import Token

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            try:
                user = CustomUser.objects.get(username=login)
                if not user.check_password(password):
                    raise forms.ValidationError('Неверный логин или пароль.')
                
                token, _ = Token.objects.get_or_create(user=user)
                user.token = token.key
                user.save()
            except CustomUser.DoesNotExist:
                raise forms.ValidationError('Пользователь с таким логином не найден.')
        return cleaned_data
