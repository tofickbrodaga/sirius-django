# Generated by Django 4.2.7 on 2024-06-13 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biobaseapp', '0003_remove_customuser_access_customuser_token_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cultivationplanning',
            old_name='started_by',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='strainprocessing',
            old_name='responsible',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='substanceidentification',
            old_name='identified_by',
            new_name='created_by',
        ),
    ]
