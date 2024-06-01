from rest_framework import serializers

from .models import (CultivationPlanning, Cultures, CustomUser, Experiments,
                     Projects, StrainProcessing, Strains,
                     SubstanceIdentification)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class StrainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strains
        fields = '__all__'


class StrainProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrainProcessing
        fields = '__all__'


class SubstanceIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceIdentification
        fields = '__all__'


class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiments
        fields = '__all__'


class CultivationPlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivationPlanning
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class CulturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultures
        fields = '__all__'
