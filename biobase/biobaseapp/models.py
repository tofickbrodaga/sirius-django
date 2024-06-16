"""Models for biobaseapp."""
import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

MAX_255 = 255
MAX_100 = 100
MAX_50 = 50


def validate_date_future(current):
    """
    Validate if the given date is in the future.

    Args:
        current: A date to be validated.

    Raises:
        ValidationError: If the date is in the future.
    """
    if current > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')


def validate_end_date_not_before_start_date(current, start_date):
    """
    Validate that the end date is not before the start date.

    Args:
        current (datetime.date): The current date.
        start_date (datetime.date): The start date.

    Raises:
        ValidationError: If the end date is before the start date.
    """
    if current < start_date:
        raise ValidationError('End date cannot be before start date.')


def validate_date(current):
    """
    Validate if the given date is of type datetime.date.

    Args:
        current: The date to be validated.

    Raises:
        ValidationError: If the date is not of type datetime.date.
    """
    if not isinstance(current, datetime.date):
        raise ValidationError('Invalid date.')


class CustomUser(AbstractUser):
    """
    Custom user model for biobase application.

    Attributes:
        token (str): The token for the user.

    """

    token = models.CharField(max_length=MAX_100, blank=True)

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            str: The string representation of the user.
        """
        return f'{self.first_name} {self.last_name}'


class Strains(models.Model):
    """
    Model for storing strains information.

    Attributes:
        id (UUIDField): The unique identifier for the strain.
        UIN (CharField): The unique identifier number for the strain.
        name (CharField): The name of the strain.
        pedigree (TextField): The information about the strain's pedigree.
        mutations (TextField): The information about the strain's mutations.
        transformations (TextField): The information about the strain's transformations.
        creation_date (DateField): The date when the strain was created.
        created_by (ForeignKey): The user who created the strain.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UIN = models.CharField(max_length=MAX_255)
    name = models.CharField(max_length=MAX_255)
    pedigree = models.TextField()
    mutations = models.TextField()
    transformations = models.TextField()
    creation_date = models.DateField(validators=[validate_date, validate_date_future])
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a string representation of the strain.

        Returns:
            str: The string representation of the strain.
        """
        return f'{self.UIN}'


class StrainProcessing(models.Model):
    """
    Model for storing strain processing information.

    Attributes:
        id (UUIDField): The unique identifier for the strain processing.
        strain_id (ForeignKey): The related strain.
        processing_date (DateField): The date of the processing.
        description (TextField): The description of the processing.
        created_by (ForeignKey): The user who created the processing.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    processing_date = models.DateField(validators=[validate_date, validate_date_future])
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class SubstanceIdentification(models.Model):
    """
    Model for storing substance identification information.

    Attributes:
        id (UUIDField): The unique identifier for the substance identification.
        strain_id (ForeignKey): The related strain.
        identification_date (DateField): The date of the identification.
        results (TextField): The results of the identification.
        created_by (ForeignKey): The user who created the identification.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    identification_date = models.DateField(validators=[validate_date, validate_date_future])
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Experiments(models.Model):
    """
    Model for storing experiments information.

    Attributes:
        id (UUIDField): The unique identifier for the experiment.
        strain_UIN (ForeignKey): The related strain.
        start_date (DateField): The start date of the experiment.
        end_date (DateField): The end date of the experiment.
        growth_medium (TextField): The growth medium used in the experiment.
        results (TextField): The results of the experiment.
        created_by (ForeignKey): The user who created the experiment.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_UIN = models.ForeignKey(Strains, on_delete=models.CASCADE)
    start_date = models.DateField(validators=[validate_date, validate_date_future])
    end_date = models.DateField(validators=[validate_date])
    growth_medium = models.TextField()
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def clean(self):
        """
        Validate the start and end dates of the experiment.

        Raises:
        ValidationError: If the end date is before the start date.
        """
        if self.start_date and self.end_date:
            validate_end_date_not_before_start_date(self.end_date, self.start_date)


class CultivationPlanning(models.Model):
    """
    Model for storing cultivation planning information.

    Attributes:
        id (UUIDField): The unique identifier for the planning.
        strain_ID (ForeignKey): The related strain.
        planning_date (DateField): The date of the planning.
        completion_date (DateField): The date of the completion.
        growth_medium (TextField): The growth medium used in the planning.
        status (TextField): The status of the planning.
        created_by (ForeignKey): The user who created the planning.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_ID = models.ForeignKey(Strains, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date, validate_date_future])
    completion_date = models.DateField(validators=[validate_date])
    growth_medium = models.TextField()
    status = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def clean(self):
        """
        Validate the completion and planning dates of the planning.

        Raises:
        ValidationError: If the completion date is before the planning date.
        """
        if self.completion_date and self.planning_date:
            validate_end_date_not_before_start_date(self.completion_date, self.planning_date)


class Projects(models.Model):
    """
    Model for storing projects information.

    Attributes:
        id (UUIDField): The unique identifier for the project.
        project_name (CharField): The name of the project.
        start_date (DateField): The start date of the project.
        end_date (DateField): The end date of the project.
        results (TextField): The results of the project.
        created_by (ForeignKey): The user who created the project.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=MAX_50)
    start_date = models.DateField(validators=[validate_date_future, validate_date])
    end_date = models.DateField(validators=[validate_date], null=True)
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a string representation of the project.

        Returns:
            str: The string representation of the project.
        """
        return f'{self.project_name}'

    def clean(self):
        """
        Validate the start and end dates of the project.

        Raises:
        ValidationError: If the end date is before the start date.
        """
        if self.start_date and self.end_date:
            validate_end_date_not_before_start_date(self.end_date, self.start_date)


class Cultures(models.Model):
    """
    Model for storing cultures information.

    Attributes:
        id (UUIDField): The unique identifier for the culture.
        project_id (ForeignKey): The related project.
        planning_date (DateField): The date of the planning.
        results (TextField): The results of the cultivation.
        created_by (ForeignKey): The user who created the culture.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date_future, validate_date])
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
