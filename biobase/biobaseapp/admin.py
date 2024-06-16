"""Custom admin classes for the biobaseapp app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (CultivationPlanning, Cultures, CustomUser, Experiments,
                     Projects, StrainProcessing, Strains,
                     SubstanceIdentification)


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin class.

    This class extends the default UserAdmin class and sets the
    add_form and form attributes to use the CustomUserCreationForm
    and CustomUserChangeForm respectively. Additionally, it sets the
    model attribute to CustomUser and the list_display attribute to
    show the email and username fields.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Strains)
class StrainsAdmin(admin.ModelAdmin):
    """
    Strains admin class.

    This class sets the list display to show the id, UIN, name, pedigree,
    creation date, and created by fields. It also sets the list filter
    to show the creation date and created by fields, and the search
    fields to show the UIN and name fields.
    """

    list_display = ('id', 'UIN', 'name', 'pedigree', 'creation_date', 'created_by')
    list_filter = ('creation_date', 'created_by')
    search_fields = ('UIN', 'name')


@admin.register(StrainProcessing)
class StrainProcessingAdmin(admin.ModelAdmin):
    """
    StrainProcessing admin class.

    This class sets the list display to show the id, strain_id, processing_date,
    and created_by fields. It also sets the list filter to show the processing_date
    and created_by fields, and the search fields to show the strain_id__UIN field.
    """

    list_display = ('id', 'strain_id', 'processing_date', 'created_by')
    list_filter = ('processing_date', 'created_by')
    search_fields = ('strain_id__UIN',)


@admin.register(SubstanceIdentification)
class SubstanceIdentificationAdmin(admin.ModelAdmin):
    """
    SubstanceIdentification admin class.

    This class sets the list display to show the id, strain_id, identification_date,
    and created_by fields. It also sets the list filter to show the identification_date
    and created_by fields, and the search fields to show the strain_id__UIN field.
    """

    list_display = ('id', 'strain_id', 'identification_date', 'created_by')
    list_filter = ('identification_date', 'created_by')
    search_fields = ('strain_id__UIN',)


@admin.register(Experiments)
class ExperimentsAdmin(admin.ModelAdmin):
    """
    Experiments admin class.

    This class sets the list display to show the id, strain_UIN, start_date,
    end_date, and created_by fields. It also sets the list filter to show the
    start_date, end_date, and created_by fields, and the search fields to show
    the strain_UIN__UIN field.
    """

    list_display = ('id', 'strain_UIN', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date', 'created_by')
    search_fields = ('strain_UIN__UIN',)


@admin.register(CultivationPlanning)
class CultivationPlanningAdmin(admin.ModelAdmin):
    """
    CultivationPlanning admin class.

    This class sets the list display to show the id, strain_ID, planning_date,
    completion_date, status, and created_by fields. It also sets the list filter
    to show the planning_date, completion_date, status, and created_by fields,
    and the search fields to show the strain_ID field.
    """

    list_display = ('id', 'strain_ID', 'planning_date', 'completion_date', 'status', 'created_by')
    list_filter = ('planning_date', 'completion_date', 'status', 'created_by')
    search_fields = ('strain_ID',)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    """
    Projects admin class.

    This class sets the list display to show the id, project_name, start_date,
    end_date, and created_by fields. It also sets the list filter to show the
    start_date, end_date, and created_by fields, and the search fields to show
    the project_name field.
    """

    list_display = ('id', 'project_name', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date', 'created_by')
    search_fields = ('project_name',)


@admin.register(Cultures)
class CulturesAdmin(admin.ModelAdmin):
    """
    Cultures admin class.

    This class sets the list display to show the id, project_id, planning_date,
    and created_by fields. It also sets the list filter to show the planning_date
    and created_by fields, and the search fields to show the project_id field.
    """

    list_display = ('id', 'project_id', 'planning_date', 'created_by')
    list_filter = ('planning_date', 'created_by')
    search_fields = ('project_id',)
