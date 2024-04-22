from django import forms
from .models import Users

class LoginForm(forms.Form):
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            try:
                user = Users.objects.get(login=login)
                if user.password != password:
                    raise forms.ValidationError("Неверный логин или пароль.")
            except Users.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким логином не найден.")
        return cleaned_data