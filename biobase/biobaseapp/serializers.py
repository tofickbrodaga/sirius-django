"""Serializers for biobaseapp."""
from rest_framework import serializers

from .models import (CultivationPlanning, Cultures, CustomUser, Experiments,
                     Projects, StrainProcessing, Strains,
                     SubstanceIdentification)

ALL = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""

    class Meta:
        model = CustomUser
        fields = ALL


class StrainsSerializer(serializers.ModelSerializer):
    """Serializer for Strains model."""

    class Meta:
        model = Strains
        fields = ALL


class StrainProcessingSerializer(serializers.ModelSerializer):
    """Serializer for StrainProcessing model."""

    class Meta:
        model = StrainProcessing
        fields = ALL


class SubstanceIdentificationSerializer(serializers.ModelSerializer):
    """Serializer for SubstanceIdentification model."""

    class Meta:
        model = SubstanceIdentification
        fields = ALL


class ExperimentsSerializer(serializers.ModelSerializer):
    """Serializer for Experiments model."""

    class Meta:
        model = Experiments
        fields = ALL


class CultivationPlanningSerializer(serializers.ModelSerializer):
    """Serializer for CultivationPlanning model."""

    class Meta:
        model = CultivationPlanning
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    """Serializer for Projects model."""

    class Meta:
        model = Projects
        fields = ALL


class CulturesSerializer(serializers.ModelSerializer):
    """Serializer for Cultures model."""

    class Meta:
        model = Cultures
        fields = ALL
