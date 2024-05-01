"""
URL configuration for biobase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from biobaseapp.views import login_view, home_page, StrainViewSet, StrainProcessingViewSet, SubstanceViewSet, ExperimentsViewSet, CultivationViewSet, ProjectsViewSet, CulturesViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'strains', StrainViewSet)
router.register(r'strain_processing', StrainProcessingViewSet)
router.register(r'substance_identification', SubstanceViewSet)
router.register(r'experiments', ExperimentsViewSet)
router.register(r'cultivation_planning', CultivationViewSet)
router.register(r'projects', ProjectsViewSet)
router.register(r'cultures', CulturesViewSet)

urlpatterns = [
    path('', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('home/', home_page, name='index'),
    path('api/', include(router.urls), name='api'),
]

