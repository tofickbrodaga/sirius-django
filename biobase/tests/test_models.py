from django.test import TestCase
from django.utils import timezone
from biobaseapp.models import Strains, StrainProcessing, SubstanceIdentification, Experiments, CultivationPlanning, Projects, Cultures
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN="UIN12345",
            name="Test Strain",
            pedigree="Pedigree info",
            mutations="Mutations info",
            transformations="Transformations info",
            creation_date=timezone.now().date(),
            created_by=self.user
        )

    def test_strain_creation(self):
        strain = Strains.objects.get(UIN="UIN12345")
        self.assertEqual(strain.name, "Test Strain")

    def test_strain_processing_creation(self):
        processing = StrainProcessing.objects.create(
            strain_id=self.strain,
            processing_date=timezone.now().date(),
            description="Processing info",
            created_by=self.user
        )
        self.assertEqual(processing.description, "Processing info")

    def test_substance_identification_creation(self):
        identification = SubstanceIdentification.objects.create(
            strain_id=self.strain,
            identification_date=timezone.now().date(),
            results="Identification results",
            created_by=self.user
        )
        self.assertEqual(identification.results, "Identification results")

    def test_experiments_creation(self):
        experiment = Experiments.objects.create(
            strain_UIN=self.strain,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            growth_medium="Growth medium info",
            results="Experiment results",
            created_by=self.user
        )
        self.assertEqual(experiment.results, "Experiment results")

    def test_cultivation_planning_creation(self):
        planning = CultivationPlanning.objects.create(
            strain_ID=self.strain,
            planning_date=timezone.now().date(),
            completion_date=timezone.now().date(),
            growth_medium="Growth medium info",
            status="Planned",
            created_by=self.user
        )
        self.assertEqual(planning.status, "Planned")

    def test_projects_creation(self):
        project = Projects.objects.create(
            project_name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            results="Project results",
            created_by=self.user
        )
        self.assertEqual(project.project_name, "Test Project")

    def test_cultures_creation(self):
        project = Projects.objects.create(
            project_name="Test Project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            results="Project results",
            created_by=self.user
        )
        culture = Cultures.objects.create(
            project_id=project,
            planning_date=timezone.now().date(),
            results="Culture results",
            created_by=self.user
        )
        self.assertEqual(culture.results, "Culture results")
