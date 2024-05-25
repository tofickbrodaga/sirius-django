from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
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

