from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def validate_date_not_in_future(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')

class CustomUser(AbstractUser):
    access = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Strains(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UIN = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pedigree = models.TextField()
    mutations = models.TextField()
    transformations = models.TextField()
    creation_date = models.DateField(validators=[validate_date_not_in_future])
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.UIN}'


class StrainProcessing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    processing_date = models.DateField(validators=[validate_date_not_in_future])
    description = models.TextField()
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class SubstanceIdentification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    identification_date = models.DateField(validators=[validate_date_not_in_future])
    results = models.TextField()
    identified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Experiments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_UIN = models.ForeignKey(Strains, on_delete=models.CASCADE)
    start_date = models.DateField(validators=[validate_date_not_in_future])
    end_date = models.DateField()
    growth_medium = models.TextField()
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class CultivationPlanning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_ID = models.ForeignKey(Strains, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date_not_in_future])
    completion_date = models.DateField()
    growth_medium = models.TextField()
    status = models.TextField()
    started_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=50)
    start_date = models.DateField(validators=[validate_date_not_in_future])
    end_date = models.DateField()
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.project_name}'


class Cultures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    planning_date = models.DateField(validators=[validate_date_not_in_future])
    results = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

