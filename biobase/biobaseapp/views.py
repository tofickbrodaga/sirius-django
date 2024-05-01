from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from rest_framework import viewsets, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from typing import Callable


from .forms import LoginForm
from .models import CustomUser, Strains, StrainProcessing, SubstanceIdentification, Experiments, CultivationPlanning, Projects, Cultures
from .serializers import CustomUserSerializer, StrainsSerializer, StrainProcessingSerializer, SubstanceIdentificationSerializer, ExperimentsSerializer, CultivationPlanningSerializer, ProjectsSerializer, CulturesSerializer

safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'

def check_auth(view: Callable) -> Callable:
    def new_view(request):
        if not (request.user and request.user.is_authenticated):
            return redirect('unauthorized')
        return view(request)
    return new_view

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication]

    return ViewSet

StrainViewSet = create_viewset(Strains, StrainsSerializer)
StrainProcessingViewSet = create_viewset(StrainProcessing, StrainProcessingSerializer)
SubstanceViewSet = create_viewset(SubstanceIdentification, SubstanceIdentificationSerializer)
ExperimentsViewSet = create_viewset(Experiments, ExperimentsSerializer)
CultivationViewSet = create_viewset(CultivationPlanning, CultivationPlanningSerializer)
ProjectsViewSet = create_viewset(Projects, ProjectsSerializer)
CulturesViewSet = create_viewset(Cultures, CulturesSerializer)


def home_page(request):
    data = {
        'message': 'Добро пожаловать на домашнюю страницу!'
    }
    context = {
        'data': data
    }
    return render(request, 'index.html', context)


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
