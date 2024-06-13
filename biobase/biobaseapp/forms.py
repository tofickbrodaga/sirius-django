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
        return super().clean()

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name in ['created_by', 'responsible', 'identified_by', 'started_by']:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.HiddenInput()
                if not self.instance.pk:
                    self.fields[field_name].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            for field_name in ['created_by', 'responsible', 'identified_by', 'started_by']:
                if hasattr(instance, field_name):
                    setattr(instance, field_name, self.user)
        if commit:
            instance.save()
        return instance

class StrainsForm(BaseModelForm):
    class Meta:
        model = Strains
        fields = '__all__'

class StrainProcessingForm(BaseModelForm):
    class Meta:
        model = StrainProcessing
        fields = '__all__'

class SubstanceIdentificationForm(BaseModelForm):
    class Meta:
        model = SubstanceIdentification
        fields = '__all__'

class ExperimentsForm(BaseModelForm):
    class Meta:
        model = Experiments
        fields = '__all__'

class CultivationPlanningForm(BaseModelForm):
    class Meta:
        model = CultivationPlanning
        fields = '__all__'

class ProjectsForm(BaseModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

class CulturesForm(BaseModelForm):
    class Meta:
        model = Cultures
        fields = '__all__'

CustomUserFormSet = modelformset_factory(CustomUser, form=CustomUserChangeForm, extra=0)
StrainsFormSet = modelformset_factory(Strains, form=StrainsForm, extra=0)
StrainProcessingFormSet = modelformset_factory(StrainProcessing, form=StrainProcessingForm, extra=0)
SubstanceIdentificationFormSet = modelformset_factory(SubstanceIdentification, form=SubstanceIdentificationForm, extra=0)
ExperimentsFormSet = modelformset_factory(Experiments, form=ExperimentsForm, extra=0)
CultivationPlanningFormSet = modelformset_factory(CultivationPlanning, form=CultivationPlanningForm, extra=0)
ProjectsFormSet = modelformset_factory(Projects, form=ProjectsForm, extra=0)
CulturesFormSet = modelformset_factory(Cultures, form=CulturesForm, extra=0)
