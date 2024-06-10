from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from biobaseapp.models import Strains, Projects, CultivationPlanning, SubstanceIdentification, Experiments
from django.utils import timezone

User = get_user_model()

class MainMenuViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN="UIN12345",
            name="Test Strain",
            pedigree="Pedigree info",
            mutations="Mutations info",
            transformations="Transformations info",
            creation_date='2024-01-01',
            created_by=self.user
        )
        self.plan = CultivationPlanning.objects.create(
            strain_ID=self.strain,
            planning_date='2024-01-01',
            completion_date='2024-01-10',
            growth_medium="Medium info",
            status="Planned",
            started_by=self.user
        )
        self.identification = SubstanceIdentification.objects.create(
            strain_id=self.strain,
            identification_date='2024-01-01',
            results="Identification results",
            identified_by=self.user
        )
        self.experiment = Experiments.objects.create(
            strain_UIN=self.strain,
            start_date='2024-01-01',
            end_date='2024-01-10',
            growth_medium="Growth medium info",
            results="Experiment results",
            created_by=self.user
        )
        self.project = Projects.objects.create(
            project_name="Test Project",
            start_date='2024-01-01',
            end_date='2024-01-10',
            results="Project results",
            created_by=self.user
        )

    def test_main_menu_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, "Test Strain")
        self.assertContains(response, "Planned")
        self.assertContains(response, "Identification results")
        self.assertContains(response, "Experiment results")
        self.assertContains(response, "Test Project")


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Форма неверно заполнена.')

    def test_login_view_post_invalid_form(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Форма неверно заполнена.')


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN="UIN12345",
            name="Test Strain",
            pedigree="Pedigree info",
            mutations="Mutations info",
            transformations="Transformations info",
            creation_date=timezone.now().date(),
            created_by=self.user
        )

    def test_strains_list_view(self):
        response = self.client.get(reverse('strains_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'strains_list.html')

    def test_cultivation_planning_list_view(self):
        response = self.client.get(reverse('planning_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planning_list.html')

    def test_experiments_list_view(self):
        response = self.client.get(reverse('experiments_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experiments_list.html')

    def test_main_menu_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class CreateAllViewTests(TestCase):
    def setUp(self):
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
            'created_by': self.user.id
        }

    def test_create_all_get(self):
        response = self.client.get(reverse('create_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_all.html')

    def test_create_all_post_valid_data(self):
        response = self.client.post(reverse('create_all'), {
            'model': 'strains',
            'strains-UIN': self.strains_data['UIN'],
            'strains-name': self.strains_data['name'],
            'strains-pedigree': self.strains_data['pedigree'],
            'strains-mutations': self.strains_data['mutations'],
            'strains-transformations': self.strains_data['transformations'],
            'strains-creation_date': self.strains_data['creation_date'],
            'strains-created_by': self.strains_data['created_by'],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Strains.objects.filter(UIN='UIN12345').exists())

    def test_create_all_post_invalid_model(self):
        response = self.client.post(reverse('create_all'), {
            'model': 'invalid_model'
        })
        self.assertEqual(response.status_code, 400)


class ChooseModelViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_choose_model_get(self):
        response = self.client.get(reverse('choose_model'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choose_model.html')

    def test_choose_model_post(self):
        response = self.client.post(reverse('choose_model'), {
            'model': 'Strains'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('choose_object', kwargs={'model_name': 'Strains'}))


class ChooseObjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN="UIN12345",
            name="Test Strain",
            pedigree="Pedigree info",
            mutations="Mutations info",
            transformations="Transformations info",
            creation_date='2024-01-01',
            created_by=self.user
        )

    def test_choose_object_get(self):
        response = self.client.get(reverse('choose_object', kwargs={'model_name': 'Strains'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choose_object.html')
        self.assertContains(response, 'Strain')

    def test_choose_object_post(self):
        response = self.client.post(reverse('choose_object', kwargs={'model_name': 'Strains'}), {
            'object_id': self.strain.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_model', kwargs={'model_name': 'Strains', 'object_id': self.strain.id}))


class EditModelViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.strain = Strains.objects.create(
            UIN="UIN12345",
            name="Test Strain",
            pedigree="Pedigree info",
            mutations="Mutations info",
            transformations="Transformations info",
            creation_date='2024-01-01',
            created_by=self.user
        )

    def test_edit_model_get(self):
        response = self.client.get(reverse('edit_model', kwargs={'model_name': 'Strains', 'object_id': self.strain.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_model.html')
        self.assertContains(response, 'Strain')

    def test_edit_model_post_valid_data(self):
        response = self.client.post(reverse('edit_model', kwargs={'model_name': 'Strains', 'object_id': self.strain.id}), {
            'strains-UIN': 'UIN12345',
            'strains-name': 'Updated Test Strain',
            'strains-pedigree': 'Updated Pedigree info',
            'strains-mutations': 'Updated Mutations info',
            'strains-transformations': 'Updated Transformations info',
            'strains-creation_date': '2024-01-01',
            'strains-created_by': self.user.id,
        })
        self.assertEqual(response.status_code, 200) 
        self.strain.refresh_from_db()
        self.assertEqual(self.strain.name, 'Test Strain')

    def test_edit_model_post_invalid_data(self):
        response = self.client.post(reverse('edit_model', kwargs={'model_name': 'Strains', 'object_id': self.strain.id}), {
            'strains-UIN': 'UIN-2020',
            'strains-name': 'Updated Test Strain',
            'strains-pedigree': 'Updated Pedigree info',
            'strains-mutations': 'Updated Mutations info',
            'strains-transformations': 'Updated Transformations info',
            'strains-creation_date': '2024-01-01',
            'strains-created_by': self.user.id,
        })
        self.assertEqual(response.status_code, 200)