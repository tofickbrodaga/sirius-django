from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelformset_factory
from rest_framework.authtoken.models import Token

from .models import (CultivationPlanning, Cultures, CustomUser, Experiments,
                     Projects, StrainProcessing, Strains,
                     SubstanceIdentification)

ALL = '__all__'
CREATED = 'created_by'

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


User = get_user_model()


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
        self.validate_username_and_password(cleaned_data)
        return cleaned_data

    def validate_username_and_password(self, cleaned_data):
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.validate_user(username, password)

    def validate_user(self, username, password):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('Пользователь с таким логином не найден.')

        if not user.check_password(password):
            raise forms.ValidationError('Неверный логин или пароль.')

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        user.save()


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_name = CREATED
        if field_name in self.fields:
            self.fields[field_name].widget = forms.HiddenInput()
            if not self.instance.pk:
                self.fields[field_name].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        field_name = CREATED
        if self.user:
            if field_name in self.fields:
                if hasattr(instance, field_name) and not getattr(instance, field_name):
                    setattr(instance, field_name, self.user)
        if commit:
            instance.save()
        return instance


class StrainsForm(BaseModelForm):
    class Meta:
        model = Strains
        fields = ALL


class StrainProcessingForm(BaseModelForm):
    class Meta:
        model = StrainProcessing
        fields = ALL

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.responsible:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class SubstanceIdentificationForm(BaseModelForm):
    class Meta:
        model = SubstanceIdentification
        fields = ALL


class ExperimentsForm(BaseModelForm):
    class Meta:
        model = Experiments
        fields = ALL

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CultivationPlanningForm(BaseModelForm):
    class Meta:
        model = CultivationPlanning
        fields = ALL

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class ProjectsForm(BaseModelForm):
    class Meta:
        model = Projects
        fields = ALL

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CulturesForm(BaseModelForm):
    class Meta:
        model = Cultures
        fields = ALL

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


CustomUserFormSet = modelformset_factory(User, form=CustomUserChangeForm, extra=0)
StrainsFormSet = modelformset_factory(Strains, form=StrainsForm, extra=0)
StrainProcessingFormSet = modelformset_factory(StrainProcessing, form=StrainProcessingForm,
                                               extra=0)
SubstanceIdentificationFormSet = modelformset_factory(SubstanceIdentification,
                                                      form=SubstanceIdentificationForm, extra=0)
ExperimentsFormSet = modelformset_factory(Experiments, form=ExperimentsForm, extra=0)
CultivationPlanningFormSet = modelformset_factory(CultivationPlanning,
                                                  form=CultivationPlanningForm, extra=0)
ProjectsFormSet = modelformset_factory(Projects, form=ProjectsForm, extra=0)
CulturesFormSet = modelformset_factory(Cultures, form=CulturesForm, extra=0)
