"""Custom forms for the biobaseapp app."""
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
    """
    Form for selecting a model and an object ID.

    This form allows the user to select a model from a list of choices
    and provide an object ID. The model choices are fixed and include
    the names of all the models in the biobaseapp app.

    Attributes:
        model (forms.ChoiceField): A choice field for selecting a model.
        object_id (forms.CharField): ACharField for entering an object ID.
    """

    model = forms.ChoiceField(choices=MODEL_CHOICES)
    object_id = forms.CharField(max_length=100)


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new CustomUser.

    This form allows the user to enter a username and email and create a new
    CustomUser. The username must be unique and the email must be valid.

    Attributes:
        username (forms.CharField): ACharField for entering a username.
        email (forms.EmailField): An EmailField for entering an email.
    """

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing the details of a CustomUser.

    This form allows the user to change the details of a CustomUser,
    including their first name, last name, and email address.

    Attributes:
        first_name (forms.CharField): ACharField for entering a first name.
        last_name (forms.CharField): ACharField for entering a last name.
        email (forms.EmailField): An EmailField for entering an email.
    """

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class LoginForm(forms.Form):
    """
    Form for logging in a user.

    This form allows the user to enter their username and password and log in.
    The username must exist in the database and the password must be correct.

    Attributes:
        username (forms.CharField): ACharField for entering a username.
        password (forms.CharField): ACharField for entering a password.
    """

    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        """
        Validate the username and password.

        This method validates the username and password entered by the user.
        It checks that the username exists in the database and that the password
        is correct. If the username and password are valid, it sets the user's
        token and saves the user.

        Returns:
            dict: The cleaned data.
        """
        cleaned_data = super().clean()
        self.validate_username_and_password(cleaned_data)
        return cleaned_data

    def validate_username_and_password(self, cleaned_data):
        """
        Validate the username and password.

        This method validates the username and password entered by the user.
        It checks that the username exists in the database and that the password
        is correct. If the username and password are valid, it sets the user's
        token and saves the user.

        Args:
            cleaned_data (dict): The cleaned data.
        """
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.validate_user(username, password)

    def validate_user(self, username, password):
        """
        Validate the user.

        This method validates the user entered by the user. It checks that the
        user exists in the database and that the password is correct. If the
        user and password are valid, it sets the user's token and saves the user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Raises:
            ValidationError: If the user does not exist or the password is incorrect.
        """
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
    """
    Base model form for forms that save data to the database.

    This class provides a way to save data to the database while
    setting the user who created the entry.

    Attributes:
        user (CustomUser): The user who is creating the entry.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with the given arguments.

        Args:
            args: positional argument list.
            kwargs: keyword arguments.

        Returns:
        None.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        field_name = CREATED
        if field_name in self.fields:
            self.fields[field_name].widget = forms.HiddenInput()
            if not self.instance.pk:
                self.fields[field_name].required = True

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
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
    """Form for creating or updating a Strains model instance."""

    class Meta:
        model = Strains
        fields = ALL


class StrainProcessingForm(BaseModelForm):
    """Form for creating or updating a StrainProcessing model instance."""

    class Meta:
        model = StrainProcessing
        fields = ALL

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
        instance = super().save(commit=False)
        if self.user and not instance.responsible:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class SubstanceIdentificationForm(BaseModelForm):
    """Form for creating or updating a SubstanceIdentification model instance."""

    class Meta:
        model = SubstanceIdentification
        fields = ALL


class ExperimentsForm(BaseModelForm):
    """Form for creating or updating a Experiments model instance."""

    class Meta:
        model = Experiments
        fields = ALL

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CultivationPlanningForm(BaseModelForm):
    """Form for creating or updating a CultivationPlanning model instance."""

    class Meta:
        model = CultivationPlanning
        fields = ALL

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class ProjectsForm(BaseModelForm):
    """Form for creating or updating a Projects model instance."""

    class Meta:
        model = Projects
        fields = ALL

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
        instance = super().save(commit=False)
        if self.user and not instance.created_by:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CulturesForm(BaseModelForm):
    """Form for creating or updating a Cultures model instance."""

    class Meta:
        model = Cultures
        fields = ALL

    def save(self, commit=True):
        """
        Save the form data to the database.

        Args:
            commit (bool, optional): Whether to save the changes to the database. Defaults to True.

        Returns:
            The saved instance of the model.
        """
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
