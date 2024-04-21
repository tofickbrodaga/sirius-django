from django.contrib import admin

from .models import Users, Strains, SubstanceIdentification, Projects, StrainProcessing, CultivationPlanning, Projects, Cultures

# Register your models here.
admin.site.register(Users)
admin.site.register(Strains)
admin.site.register(StrainProcessing)
admin.site.register(SubstanceIdentification)
admin.site.register(CultivationPlanning)
admin.site.register(Projects)
admin.site.register(Cultures)