"""Test for models in the biobaseapp app."""
from biobaseapp.models import (CultivationPlanning, Cultures, Experiments,
                               Projects, StrainProcessing, Strains,
                               SubstanceIdentification)

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ModelTests(TestCase):
    """Tests for the models in the biobaseapp app."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN='UIN12345',
            name='Test Strain',
            pedigree='Pedigree info',
            mutations='Mutations info',
            transformations='Transformations info',
            creation_date=timezone.now().date(),
            created_by=self.user,
        )

    def test_strain_creation(self):
        """Test that a strain can be created."""
        strain = Strains.objects.get(UIN='UIN12345')
        self.assertEqual(strain.name, 'Test Strain')

    def test_strain_processing_creation(self):
        """Test that a strain processing can be created."""
        processing = StrainProcessing.objects.create(
            strain_id=self.strain,
            processing_date=timezone.now().date(),
            description='Processing info',
            created_by=self.user,
        )
        self.assertEqual(processing.description, 'Processing info')

    def test_substance_identification_creation(self):
        """Test that a substance identification can be created."""
        identification = SubstanceIdentification.objects.create(
            strain_id=self.strain,
            identification_date=timezone.now().date(),
            results='Identification results',
            created_by=self.user,
        )
        self.assertEqual(identification.results, 'Identification results')

    def test_experiments_creation(self):
        """Test that an experiment can be created."""
        experiment = Experiments.objects.create(
            strain_UIN=self.strain,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            growth_medium='Growth medium info',
            results='Experiment results',
            created_by=self.user,
        )
        self.assertEqual(experiment.results, 'Experiment results')

    def test_cultivation_planning_creation(self):
        """Test that cultivation planning can be created."""
        planning = CultivationPlanning.objects.create(
            strain_ID=self.strain,
            planning_date=timezone.now().date(),
            completion_date=timezone.now().date(),
            growth_medium='Growth medium info',
            status='Planned',
            created_by=self.user,
        )
        self.assertEqual(planning.status, 'Planned')

    def test_projects_creation(self):
        """Test that a project can be created."""
        project = Projects.objects.create(
            project_name='Test Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            results='Project results',
            created_by=self.user,
        )
        self.assertEqual(project.project_name, 'Test Project')

    def test_cultures_creation(self):
        """Test that a culture can be created."""
        project = Projects.objects.create(
            project_name='Test Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            results='Project results',
            created_by=self.user,
        )
        culture = Cultures.objects.create(
            project_id=project,
            planning_date=timezone.now().date(),
            results='Culture results',
            created_by=self.user,
        )
        self.assertEqual(culture.results, 'Culture results')
