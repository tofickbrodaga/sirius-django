# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def home_page(request):
        return render(request, 'index.html')


def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data
            user = authenticate(request, username=login_data['login'], password=login_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = 'Неверный логин или пароль.'
        else:
            error_message = 'Форма неверно заполнена.'
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'login.html', context)

