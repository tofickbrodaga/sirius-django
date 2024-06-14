from rest_framework import serializers

from config import ALL

from .models import (CultivationPlanning, Cultures, CustomUser, Experiments,
                     Projects, StrainProcessing, Strains,
                     SubstanceIdentification)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ALL


class StrainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strains
        fields = ALL


class StrainProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrainProcessing
        fields = ALL


class SubstanceIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceIdentification
        fields = ALL


class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiments
        fields = ALL


class CultivationPlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivationPlanning
        fields = ALL


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ALL


class CulturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultures
        fields = ALL
