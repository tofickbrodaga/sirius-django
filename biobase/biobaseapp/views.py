from typing import Callable

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission

from .forms import (CultivationPlanningForm, CulturesForm, ExperimentsForm,
                    LoginForm, ProjectsForm, StrainProcessingForm, StrainsForm,
                    SubstanceIdentificationForm)
from .models import (CultivationPlanning, Cultures, Experiments, Projects,
                     StrainProcessing, Strains, SubstanceIdentification)
from .serializers import (CultivationPlanningSerializer, CulturesSerializer,
                          ExperimentsSerializer, ProjectsSerializer,
                          StrainProcessingSerializer, StrainsSerializer,
                          SubstanceIdentificationSerializer)

ID = 'id'
POST = 'POST'
SEARCH_TYPE = 'search_type'
QUERY = 'q'
DATE_FROM = 'date_from'
DATE_TO = 'date_to'
CREATED = 'created_by'

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
SubstanceViewSet = create_viewset(
    SubstanceIdentification, SubstanceIdentificationSerializer,
)
ExperimentsViewSet = create_viewset(Experiments, ExperimentsSerializer)
CultivationViewSet = create_viewset(CultivationPlanning, CultivationPlanningSerializer)
ProjectsViewSet = create_viewset(Projects, ProjectsSerializer)
CulturesViewSet = create_viewset(Cultures, CulturesSerializer)


class StrainsListView(ListView):
    model = Strains
    template_name = 'strains_list.html'
    context_object_name = 'strains'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by(ID)
        search_type = self.request.GET.get(SEARCH_TYPE)
        query = self.request.GET.get(QUERY)
        date_from = self.request.GET.get(DATE_FROM)
        date_to = self.request.GET.get(DATE_TO)
        responsible = self.request.GET.get(CREATED)

        if search_type == 'name' and query:
            queryset = queryset.filter(name__icontains=query)
        elif search_type == 'date' and date_from and date_to:
            queryset = queryset.filter(creation_date__range=[date_from, date_to])
        elif search_type == CREATED and responsible:
            queryset = queryset.filter(created_by__username__icontains=responsible)

        return queryset


class CultivationPlanningListView(ListView):
    model = CultivationPlanning
    template_name = 'planning_list.html'
    context_object_name = 'plannings'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        search_type = self.request.GET.get('search_type')
        query = self.request.GET.get('q')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        responsible = self.request.GET.get(CREATED)

        if search_type == 'name' and query:
            queryset = queryset.filter(strain_ID__name__icontains=query)
        elif search_type == 'date' and date_from and date_to:
            queryset = queryset.filter(planning_date__range=[date_from, date_to])
        elif search_type == CREATED and responsible:
            queryset = queryset.filter(created_by__username__icontains=responsible)

        return queryset


class ExperimentsListView(ListView):
    model = Experiments
    template_name = 'experiments_list.html'
    context_object_name = 'experiments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by(ID)
        search_type = self.request.GET.get(SEARCH_TYPE)
        query = self.request.GET.get(QUERY)
        date_from = self.request.GET.get(DATE_FROM)
        date_to = self.request.GET.get(DATE_TO)
        responsible = self.request.GET.get(CREATED)

        if search_type == 'name' and query:
            queryset = queryset.filter(strain_UIN__name__icontains=query)
        elif search_type == 'date' and date_from and date_to:
            queryset = queryset.filter(start_date__range=[date_from, date_to])
        elif search_type == CREATED and responsible:
            queryset = queryset.filter(created_by__username__icontains=responsible)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_type'] = self.request.GET.get(SEARCH_TYPE, '')
        context['q'] = self.request.GET.get(QUERY, '')
        context['date_from'] = self.request.GET.get(DATE_FROM, '')
        context['date_to'] = self.request.GET.get(DATE_TO, '')
        context['responsible'] = self.request.GET.get(CREATED, '')
        return context


def main_menu(request):
    user = request.user
    strains = Strains.objects.filter(created_by=user)
    plans = CultivationPlanning.objects.filter(created_by=user)
    identifications = SubstanceIdentification.objects.filter(created_by=user)
    experiments = Experiments.objects.filter(created_by=user)
    projects = Projects.objects.filter(created_by=user)
    return render(
        request,
        'index.html',
        {
            'strains': strains,
            'plans': plans,
            'identifications': identifications,
            'experiments': experiments,
            'projects': projects,
            'user': user,
        },
    )


def login_view(request):
    error_message = None

    if request.method == POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data
            user = authenticate(
                request,
                username=login_data['username'],
                password=login_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            error_message = 'Форма неверно заполнена.'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def create_all(request):
    model_forms = {
        'strains': StrainsForm,
        'strainprocessing': StrainProcessingForm,
        'substanceidentification': SubstanceIdentificationForm,
        'experiments': ExperimentsForm,
        'cultivationplanning': CultivationPlanningForm,
        'projects': ProjectsForm,
        'cultures': CulturesForm,
    }

    if request.method == 'POST':
        selected_model = request.POST.get('model')
        if selected_model not in model_forms:
            return HttpResponseBadRequest('Неверно выбрана модель')

        form_class = model_forms[selected_model]
        form = form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect('index')

    else:
        selected_model = request.GET.get('model')
        form = (
            model_forms[selected_model](user=request.user)
            if selected_model in model_forms
            else None
        )

    return render(
        request,
        'create_all.html',
        {
            'form': form,
            'model_forms': model_forms.keys(),
            'selected_model': selected_model,
        },
    )


def choose_model(request):
    if request.method == POST:
        model_name = request.POST.get('model')
        if model_name:
            return redirect('choose_object', model_name=model_name)
    return render(
        request,
        'choose_model.html',
        {
            'models': MODEL_FORMS.keys(),
        },
    )


def choose_object(request, model_name):
    model_class = MODEL_CLASSES.get(model_name)
    if not model_class:
        return redirect('choose_model')

    object_str_methods = {
        'Strains': 'UIN',
        'StrainProcessing': 'description',
        'SubstanceIdentification': 'results',
        'Experiments': 'results',
        'CultivationPlanning': 'status',
        'Projects': 'project_name',
        'Cultures': 'id',
    }

    object_str_method = object_str_methods.get(model_name)

    if object_str_method:
        objects_model = model_class.objects.all().values_list('id', object_str_method)

    if request.method == POST:
        object_id = request.POST.get('object_id')
        if object_id:
            get_id = model_class.objects.get(pk=object_id)
            getattr(get_id, object_str_method)
            return redirect('edit_model', model_name=model_name, object_id=object_id)

    return render(
        request,
        'choose_object.html',
        {
            'model_name': model_name,
            'objects': objects_model,
        },
    )


def edit_model(request, model_name, object_id):
    form_class = MODEL_FORMS.get(model_name)
    model_class = MODEL_CLASSES.get(model_name)

    if not form_class or not model_class:
        return redirect('choose_model')

    model = get_object_or_404(model_class, id=object_id)

    if request.method == POST:
        form = form_class(request.POST, instance=model, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_model', model_name=model_name, object_id=object_id)
    else:
        form = form_class(instance=model, user=request.user)

    return render(
        request,
        'edit_model.html',
        {
            'form': form,
            'model_name': model_name,
            'object_id': object_id,
        },
    )
