from django.db import models
import uuid

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    access = models.CharField(max_length=255)


class Strains(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UIN = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pedigree = models.TextField()
    mutations = models.TextField()
    transformations = models.TextField()
    creation_date = models.DateField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class StrainProcessing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    processing_date = models.DateField()
    description = models.TextField()
    responsible = models.ForeignKey(Users, on_delete=models.CASCADE)


class SubstanceIdentification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_id = models.ForeignKey(Strains, on_delete=models.CASCADE)
    identification_date = models.DateField()
    results = models.TextField()
    identified_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Experiments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_UIN = models.ForeignKey(Strains, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    growth_medium = models.TextField()
    results = models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class CultivationPlanning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strain_ID = models.UUIDField()
    planning_date = models.DateField()
    completion_date = models.DateField()
    growth_medium = models.TextField()
    status = models.TextField()
    started_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    results = models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Cultures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    planning_date = models.DateField()
    results = models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
