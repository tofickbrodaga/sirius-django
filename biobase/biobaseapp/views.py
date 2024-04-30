# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from rest_framework import viewsets
from .models import CustomUser, Strains, StrainProcessing, SubstanceIdentification, Experiments, CultivationPlanning, Projects, Cultures
from .serializers import CustomUserSerializer, StrainsSerializer, StrainProcessingSerializer, SubstanceIdentificationSerializer, ExperimentsSerializer, CultivationPlanningSerializer, ProjectsSerializer, CulturesSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class StrainsViewSet(viewsets.ModelViewSet):
    queryset = Strains.objects.all()
    serializer_class = StrainsSerializer


class StrainProcessingViewSet(viewsets.ModelViewSet):
    queryset = StrainProcessing.objects.all()
    serializer_class = StrainProcessingSerializer


class SubstanceIdentificationViewSet(viewsets.ModelViewSet):
    queryset = SubstanceIdentification.objects.all()
    serializer_class = SubstanceIdentificationSerializer


class ExperimentsViewSet(viewsets.ModelViewSet):
    queryset = Experiments.objects.all()
    serializer_class = ExperimentsSerializer


class CultivationPlanningViewSet(viewsets.ModelViewSet):
    queryset = CultivationPlanning.objects.all()
    serializer_class = CultivationPlanningSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class CulturesViewSet(viewsets.ModelViewSet):
    queryset = Cultures.objects.all()
    serializer_class = CulturesSerializer


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
