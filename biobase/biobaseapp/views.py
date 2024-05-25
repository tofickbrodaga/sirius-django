from typing import Callable

from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission

from .forms import *
from .models import (CultivationPlanning, Cultures, Experiments, Projects,
                     StrainProcessing, Strains, SubstanceIdentification)
from .serializers import (CultivationPlanningSerializer, CulturesSerializer,
                          ExperimentsSerializer, ProjectsSerializer,
                          StrainProcessingSerializer, StrainsSerializer,
                          SubstanceIdentificationSerializer)

safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'

def check_auth(view: Callable) -> Callable:
    def new_view(request):
        if not (request.user and request.user.is_authenticated):
            return redirect('unauthorized')
        return view(request)
    return new_view

class MyPermission(BasePermission):
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
         authentication_classes = [TokenAuthentication]

     return ViewSet

StrainViewSet = create_viewset(Strains, StrainsSerializer)
StrainProcessingViewSet = create_viewset(StrainProcessing, StrainProcessingSerializer)
SubstanceViewSet = create_viewset(SubstanceIdentification, SubstanceIdentificationSerializer)
ExperimentsViewSet = create_viewset(Experiments, ExperimentsSerializer)
CultivationViewSet = create_viewset(CultivationPlanning, CultivationPlanningSerializer)
ProjectsViewSet = create_viewset(Projects, ProjectsSerializer)
CulturesViewSet = create_viewset(Cultures, CulturesSerializer)

def main_menu(request):
    user = request.user
    strains = Strains.objects.filter(created_by=user)
    plans = CultivationPlanning.objects.filter(started_by=user)
    identifications = SubstanceIdentification.objects.filter(identified_by=user)
    experiments = Experiments.objects.filter(created_by=user)
    projects = Projects.objects.filter(created_by=user)
    return render(request, 'index.html', {
        'strains': strains,
        'plans': plans,
        'identifications': identifications,
        'experiments': experiments,
        'projects': projects,
    })


def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data
            user = authenticate(request, username=login_data['username'], password=login_data['password'])
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

def create_all(request):
    model_forms = {
        'strains': StrainsForm,
        'strain_processing': StrainProcessingForm,
        'substance_identification': SubstanceIdentificationForm,
        'experiments': ExperimentsForm,
        'cultivation_planning': CultivationPlanningForm,
        'projects': ProjectsForm,
        'cultures': CulturesForm,
    }

    if request.method == 'POST':
        selected_model = request.POST.get('model')
        if selected_model not in model_forms:
            return HttpResponseBadRequest("Invalid model selected")

        form_class = model_forms[selected_model]
        form = form_class(request.POST, prefix=selected_model)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        selected_model = request.GET.get('model')
        if selected_model in model_forms:
            form_class = model_forms[selected_model]
            form = form_class(prefix=selected_model)
        else:
            form = None

    return render(request, 'create_all.html', {
        'form': form,
        'model_forms': model_forms.keys(),
        'selected_model': selected_model
    })


MODEL_FORMS = {
    'Strains': StrainsForm,
    'StrainProcessing': StrainProcessingForm,
    'SubstanceIdentification': SubstanceIdentificationForm,
    'Experiments': ExperimentsForm,
    'CultivationPlanning': CultivationPlanningForm,
    'Projects': ProjectsForm,
    'Cultures': CulturesForm,
}

MODEL_CLASSES = {
    'Strains': Strains,
    'StrainProcessing': StrainProcessing,
    'SubstanceIdentification': SubstanceIdentification,
    'Experiments': Experiments,
    'CultivationPlanning': CultivationPlanning,
    'Projects': Projects,
    'Cultures': Cultures,
}

def choose_model(request):
    if request.method == 'POST':
        model_name = request.POST.get('model')
        if model_name:
            return redirect('choose_object', model_name=model_name)
    return render(request, 'choose_model.html', {
        'models': MODEL_FORMS.keys()
    })

def choose_object(request, model_name):
    model_class = MODEL_CLASSES.get(model_name)
    if not model_class:
        return redirect('choose_model')

    objects = model_class.objects.all()
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        if object_id:
            return redirect('edit_model', model_name=model_name, object_id=object_id)

    return render(request, 'choose_object.html', {
        'model_name': model_name,
        'objects': objects,
    })

def edit_model(request, model_name, object_id):
    form_class = MODEL_FORMS.get(model_name)
    model_class = MODEL_CLASSES.get(model_name)

    if not form_class or not model_class:
        return redirect('choose_model')

    obj = get_object_or_404(model_class, id=object_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('edit_model', model_name=model_name, object_id=object_id)  # Редирект на ту же страницу после сохранения
    else:
        form = form_class(instance=obj)

    return render(request, 'edit_model.html', {
        'form': form,
        'model_name': model_name,
        'object_id': object_id,
    })