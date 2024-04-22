from django.contrib import admin
from .models import CustomUser, Strains, SubstanceIdentification, Projects, StrainProcessing, CultivationPlanning, Projects, Cultures, Experiments
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Strains)
class StrainsAdmin(admin.ModelAdmin):
    list_display = ('id', 'UIN', 'name', 'pedigree', 'creation_date', 'created_by')
    list_filter = ('creation_date', 'created_by')
    search_fields = ('UIN', 'name')

@admin.register(StrainProcessing)
class StrainProcessingAdmin(admin.ModelAdmin):
    list_display = ('id', 'strain_id', 'processing_date', 'responsible')
    list_filter = ('processing_date', 'responsible')
    search_fields = ('strain_id__UIN',)

@admin.register(SubstanceIdentification)
class SubstanceIdentificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'strain_id', 'identification_date', 'identified_by')
    list_filter = ('identification_date', 'identified_by')
    search_fields = ('strain_id__UIN',)

@admin.register(Experiments)
class ExperimentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'strain_UIN', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date', 'created_by')
    search_fields = ('strain_UIN__UIN',)

@admin.register(CultivationPlanning)
class CultivationPlanningAdmin(admin.ModelAdmin):
    list_display = ('id', 'strain_ID', 'planning_date', 'completion_date', 'status', 'started_by')
    list_filter = ('planning_date', 'completion_date', 'status', 'started_by')
    search_fields = ('strain_ID',)

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date', 'created_by')
    search_fields = ('project_name',)

@admin.register(Cultures)
class CulturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'planning_date', 'created_by')
    list_filter = ('planning_date', 'created_by')
    search_fields = ('project_id',)
