from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class LoginForm(forms.Form):
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if login and password:
            try:
                user = CustomUser.objects.get(login=login)
                if user.password != password:
                    raise forms.ValidationError("Неверный логин или пароль.")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким логином не найден.")
        return cleaned_data