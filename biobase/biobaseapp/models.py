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
    if current > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')


def validate_end_date_not_before_start_date(current, start_date):
    if current < start_date:
        raise ValidationError('End date cannot be before start date.')


def validate_date(current):
    if not isinstance(current, datetime.date):
        raise ValidationError('Invalid date.')


class CustomUser(AbstractUser):
    token = models.CharField(max_length=MAX_100, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Strains(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UIN = models.CharField(max_length=MAX_255)
    name = models.CharField(max_length=MAX_255)
    pedigree = models.TextField()
    mutations = models.TextField()
    transformations = models.TextField()
    creation_date = models.DateField(validators=[validate_date, validate_date_future])
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.UIN}'


class StrainProcessing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    processing_date = models.DateField(validators=[validate_date, validate_date_future])
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class SubstanceIdentification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    identification_date = models.DateField(validators=[validate_date, validate_date_future])
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Experiments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_UIN = models.ForeignKey(Strains, on_delete=models.CASCADE)
    start_date = models.DateField(validators=[validate_date, validate_date_future])
    end_date = models.DateField(validators=[validate_date])
    growth_medium = models.TextField()
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def clean(self):
        if self.start_date and self.end_date:
            validate_end_date_not_before_start_date(self.end_date, self.start_date)


class CultivationPlanning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_ID = models.ForeignKey(Strains, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date, validate_date_future])
    completion_date = models.DateField(validators=[validate_date])
    growth_medium = models.TextField()
    status = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def clean(self):
        if self.completion_date and self.planning_date:
            validate_end_date_not_before_start_date(self.completion_date, self.planning_date)


class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=MAX_50)
    start_date = models.DateField(validators=[validate_date_future, validate_date])
    end_date = models.DateField(validators=[validate_date], null=True)
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.project_name}'

    def clean(self):
        if self.start_date and self.end_date:
            validate_end_date_not_before_start_date(self.end_date, self.start_date)


class Cultures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date_future, validate_date])
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
