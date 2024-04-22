# Generated by Django 4.2.7 on 2024-04-22 16:42

import biobaseapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biobaseapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultivationplanning',
            name='planning_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='cultivationplanning',
            name='strain_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biobaseapp.strains'),
        ),
        migrations.AlterField(
            model_name='cultures',
            name='planning_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='experiments',
            name='start_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='projects',
            name='project_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='projects',
            name='start_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='strainprocessing',
            name='processing_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='strains',
            name='creation_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
        migrations.AlterField(
            model_name='substanceidentification',
            name='identification_date',
            field=models.DateField(validators=[biobaseapp.models.validate_date_not_in_future]),
        ),
    ]
