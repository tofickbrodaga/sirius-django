# views.py
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.cleaned_data['login']
            return redirect('home')
    else:
        form = LoginForm()

    error_message = None
    if request.method == 'POST' and not form.is_valid():
        error_message = "Неверный логин или пароль."

    return render(request, 'login.html', {'form': form, 'error_message': error_message})
