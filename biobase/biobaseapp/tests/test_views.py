"""Test views.py module."""
from biobaseapp.forms import StrainsForm
from biobaseapp.models import (CultivationPlanning, Experiments, Projects,
                               Strains, SubstanceIdentification)
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone


OK = 200
ERROR = 400
MOVED = 302

User = get_user_model()


class MainMenuViewTests(TestCase):
    """Test Main Menu View."""

    def setUp(self):
        """Set up test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN='UIN12345',
            name='Test Strain',
            pedigree='Pedigree info',
            mutations='Mutations info',
            transformations='Transformations info',
            creation_date='2024-01-01',
            created_by=self.user,
        )
        self.plan = CultivationPlanning.objects.create(
            strain_ID=self.strain,
            planning_date='2024-01-01',
            completion_date='2024-01-10',
            growth_medium='Medium info',
            status='Planned',
            created_by=self.user,
        )
        self.identification = SubstanceIdentification.objects.create(
            strain_id=self.strain,
            identifications_date='2024-01-01',
            results='Identification results',
            created_by=self.user,
        )
        self.experiment = Experiments.objects.create(
            strain_UIN=self.strain,
            start_date='2024-01-01',
            end_date='2024-01-10',
            growth_medium='Growth medium info',
            results='Experiment results',
            created_by=self.user,
        )
        self.project = Projects.objects.create(
            project_name='Test Project',
            start_date='2024-01-01',
            end_date='2024-01-10',
            results='Project results',
            created_by=self.user,
        )

    def test_main_menu_view(self):
        """Test Main Menu View returns expected data."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Test Strain')
        self.assertContains(response, 'Planned')
        self.assertContains(response, 'Identification results')
        self.assertContains(response, 'Experiment results')
        self.assertContains(response, 'Test Project')


class LoginViewTests(TestCase):
    """Tests for the Login View."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_view_get(self):
        """Test GET request to the login view."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        """Test POST request to the login view with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, MOVED)
        self.assertRedirects(response, reverse('index'))

    def test_login_view_post_invalid_credentials(self):
        """Test POST request to the login view with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Форма неверно заполнена.')

    def test_login_view_post_invalid_form(self):
        """Test POST request to the login view with an invalid form."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Форма неверно заполнена.')


class ViewTests(TestCase):
    """Tests for the views of the app."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN='UIN12345',
            name='Test Strain',
            pedigree='Pedigree info',
            mutations='Mutations info',
            transformations='Transformations info',
            creation_date=timezone.now().date(),
            created_by=self.user,
        )

    def test_strains_list_view(self):
        """Test the strains list view."""
        response = self.client.get(reverse('strains_list'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'strains_list.html')

    def test_cultivation_planning_list_view(self):
        """Test the cultivation planning list view."""
        response = self.client.get(reverse('planning_list'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'planning_list.html')

    def test_experiments_list_view(self):
        """Test the experiments list view."""
        response = self.client.get(reverse('experiments_list'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'experiments_list.html')

    def test_main_menu_view(self):
        """Test the main menu view."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view(self):
        """Test the login view."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'login.html')


class CreateAllViewTests(TestCase):
    """Tests for the CreateAllView."""

    def setUp(self):
        """Set up the test case."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strains_data = {
            'UIN': 'UIN12345',
            'name': 'Test Strain',
            'pedigree': 'Pedigree info',
            'mutations': 'Mutations info',
            'transformations': 'Transformations info',
            'creation_date': '2024-01-01',
            'created_by': self.user.id,
        }

    def test_create_all_get_valid_model(self):
        """Test the GET request with a valid model."""
        response = self.client.get(reverse('create_all'), {'model': 'strains'})
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'create_all.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], StrainsForm)

    def test_create_all_get_invalid_model(self):
        """Test the GET request with an invalid model."""
        response = self.client.get(reverse('create_all'), {'model': 'invalid_model'})
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'create_all.html')
        self.assertIsNone(response.context['form'])

    def test_create_all_post_valid_data(self):
        """Test the POST request with valid data."""
        url = reverse('create_all')
        response = self.client.post(url, {
            'model': 'strains',
            'UIN': 'UIN12345',
            'name': 'Test Strain',
            'pedigree': 'Pedigree info',
            'mutations': 'Mutations info',
            'transformations': 'Transformations info',
            'creation_date': '2024-01-01',
            'created_by': self.user.id,
        })
        self.assertEqual(response.status_code, MOVED)
        self.assertTrue(Strains.objects.filter(UIN='UIN12345').exists())

    def test_create_all_post_invalid_model(self):
        """Test the POST request with an invalid model."""
        response = self.client.post(reverse('create_all'), {
            'model': 'invalid_model',
        })
        self.assertEqual(response.status_code, ERROR)


class ChooseModelViewTests(TestCase):
    """Tests for the ChooseModelView."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_choose_model_get(self):
        """Test the GET request to ChooseModelView."""
        response = self.client.get(reverse('choose_model'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'choose_model.html')

    def test_choose_model_post(self):
        """Test the POST request to ChooseModelView."""
        response = self.client.post(reverse('choose_model'), {
            'model': 'Strains',
        })
        self.assertEqual(response.status_code, MOVED)
        self.assertRedirects(response, reverse('choose_object', kwargs={'model_name': 'Strains'}))


class ChooseObjectViewTests(TestCase):
    """Tests for the ChooseObjectView."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN='UIN12345',
            name='Test Strain',
            pedigree='Pedigree info',
            mutations='Mutations info',
            transformations='Transformations info',
            creation_date='2024-01-01',
            created_by=self.user,
        )

    def test_choose_object_get(self):
        """Test the GET request to ChooseObjectView."""
        response = self.client.get(reverse('choose_object', kwargs={'model_name': 'Strains'}))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'choose_object.html')
        self.assertContains(response, self.strain.UIN)

    def test_choose_object_post(self):
        """Test the POST request to ChooseObjectView."""
        response = self.client.post(reverse('choose_object', kwargs={'model_name': 'Strains'}), {
            'object_id': str(self.strain.id),
        })
        self.assertEqual(response.status_code, MOVED)
        self.assertRedirects(response, reverse('edit_model', kwargs={'model_name': 'Strains',
                                                                     'object_id': self.strain.id}))


class EditModelViewTests(TestCase):
    """Tests for the EditModelView."""

    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN='UIN12345',
            name='Test Strain',
            pedigree='Pedigree info',
            mutations='Mutations info',
            transformations='Transformations info',
            creation_date='2024-01-01',
            created_by=self.user,
        )

    def test_edit_model_get(self):
        """Test the GET request to EditModelView."""
        response = self.client.get(reverse('edit_model', kwargs={'model_name': 'Strains',
                                                                 'object_id': self.strain.id}))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'edit_model.html')
        self.assertContains(response, 'Strain')

    def test_edit_model_post_valid_data(self):
        """Test the POST request with valid data to EditModelView."""
        response = self.client.post(reverse('edit_model', kwargs={'model_name': 'Strains',
                                                                  'object_id': self.strain.id}), {
            'strains-UIN': 'UIN12345',
            'strains-name': 'Updated Test Strain',
            'strains-pedigree': 'Updated Pedigree info',
            'strains-mutations': 'Updated Mutations info',
            'strains-transformations': 'Updated Transformations info',
            'strains-creation_date': '2024-01-01',
            'strains-created_by': self.user.id,
        })
        self.assertEqual(response.status_code, OK)
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.name, 'Test Strain')

    def test_edit_model_post_invalid_data(self):
        """Test the POST request with invalid data to EditModelView."""
        response = self.client.post(reverse('edit_model', kwargs={'model_name': 'Strains',
                                                                  'object_id': self.strain.id}), {
            'strains-UIN': 'UIN-2020',
            'strains-name': 'Updated Test Strain',
            'strains-pedigree': 'Updated Pedigree info',
            'strains-mutations': 'Updated Mutations info',
            'strains-transformations': 'Updated Transformations info',
            'strains-creation_date': '2024-01-01',
            'strains-created_by': self.user.id,
        })
        self.assertEqual(response.status_code, OK)
