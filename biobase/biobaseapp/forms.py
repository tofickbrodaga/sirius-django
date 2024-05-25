from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelformset_factory
from rest_framework.authtoken.models import Token

from .models import *

MODEL_CHOICES = [
    ('CustomUser', 'CustomUser'),
    ('Strains', 'Strains'),
    ('StrainProcessing', 'StrainProcessing'),
    ('SubstanceIdentification', 'SubstanceIdentification'),
    ('Experiments', 'Experiments'),
    ('CultivationPlanning', 'CultivationPlanning'),
    ('Projects', 'Projects'),
    ('Cultures', 'Cultures'),
]

class ModelSelectionForm(forms.Form):
    model = forms.ChoiceField(choices=MODEL_CHOICES)
    object_id = forms.CharField(max_length=100)

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
                if not user.check_password(password):
                    raise forms.ValidationError('Неверный логин или пароль.')
                
                token, _ = Token.objects.get_or_create(user=user)
                user.token = token.key
                user.save()
            except CustomUser.DoesNotExist:
                raise forms.ValidationError('Пользователь с таким логином не найден.')
        return cleaned_data


class StrainsForm(forms.ModelForm):
    class Meta:
        model = Strains
        fields = ['UIN', 'name', 'pedigree', 'mutations', 'transformations', 'creation_date', 'created_by']

class StrainProcessingForm(forms.ModelForm):
    class Meta:
        model = StrainProcessing
        fields = ['strain_id', 'processing_date', 'description', 'responsible']

class SubstanceIdentificationForm(forms.ModelForm):
    class Meta:
        model = SubstanceIdentification
        fields = ['strain_id', 'identification_date', 'results', 'identified_by']

class ExperimentsForm(forms.ModelForm):
    class Meta:
        model = Experiments
        fields = ['strain_UIN', 'start_date', 'end_date', 'growth_medium', 'results', 'created_by']

class CultivationPlanningForm(forms.ModelForm):
    class Meta:
        model = CultivationPlanning
        fields = ['strain_ID', 'planning_date', 'completion_date', 'growth_medium', 'status', 'started_by']

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name', 'start_date', 'end_date', 'results', 'created_by']

class CulturesForm(forms.ModelForm):
    class Meta:
        model = Cultures
        fields = ['project_id', 'planning_date', 'results', 'created_by']

CustomUserFormSet = modelformset_factory(CustomUser, form=CustomUserChangeForm, extra=0)
StrainsFormSet = modelformset_factory(Strains, form=StrainsForm, extra=0)
StrainProcessingFormSet = modelformset_factory(StrainProcessing, form=StrainProcessingForm, extra=0)
SubstanceIdentificationFormSet = modelformset_factory(SubstanceIdentification, form=SubstanceIdentificationForm, extra=0)
ExperimentsFormSet = modelformset_factory(Experiments, form=ExperimentsForm, extra=0)
CultivationPlanningFormSet = modelformset_factory(CultivationPlanning, form=CultivationPlanningForm, extra=0)
ProjectsFormSet = modelformset_factory(Projects, form=ProjectsForm, extra=0)
CulturesFormSet = modelformset_factory(Cultures, form=CulturesForm, extra=0)
