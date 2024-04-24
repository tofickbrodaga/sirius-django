# Generated by Django 4.2.7 on 2024-04-24 08:03

import biobaseapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biobaseapp', '0002_alter_cultivationplanning_planning_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='access',
        ),
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='cultivationplanning',
            name='completion_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='cultivationplanning',
            name='planning_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date, biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='cultures',
            name='planning_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future, biobaseapp.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='experiments',
            name='end_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='experiments',
            name='start_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date, biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='projects',
            name='end_date',
            field=models.DateField(null=True, validators=[biobaseapp.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='projects',
            name='start_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future, biobaseapp.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='strainprocessing',
            name='processing_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date, biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='strains',
            name='creation_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date, biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='substanceidentification',
            name='identification_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date, biobaseapp.models.validate_date_not_in_future]),
        ),
    ]