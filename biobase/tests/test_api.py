from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from biobaseapp.models import Projects, Strains

CustomUser = get_user_model()

class StrainsAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/strains/'

    def api_methods(self, user: CustomUser, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'UIN': 'N877',
            'name': 'New Strain',
            'pedigree': 'xyz',
            'mutations': 'abc',
            'transformations': 'none',
            'creation_date': now().date(),
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        if response.status_code != post_exp:
            print("POST response data:", response.data)
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class StrainProcessingAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/strain_processing/'

        self.strain = Strains.objects.create(
            UIN='N876',
            name='Strain CD',
            pedigree='sdfg',
            mutations='dfg',
            transformations='none',
            creation_date=now().date(),
            created_by=self.user
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_id': strain.id,
            'processing_date': now().date(),
            'description': 'None',
            'created_by': user.id,
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        if response.status_code != post_exp:
            print("POST response data:", response.data)
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)


    def test_superuser(self):
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )


    def test_user(self):
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class SubstanceIdentificationAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/substance_identification/'

        self.strain = Strains.objects.create(
            UIN='N876',
            name='Strain CD',
            pedigree='sdfg',
            mutations='dfg',
            transformations='none',
            creation_date=now().date(),
            created_by=self.user
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_id': strain.id,
            'identification_date': now().date(),
            'results': 'Positive',
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class ExperimentsAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/experiments/'

        self.strain = Strains.objects.create(
            UIN='N876',
            name='Strain CD',
            pedigree='sdfg',
            mutations='dfg',
            transformations='none',
            creation_date=now().date(),
            created_by=self.user
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_UIN': strain.id,
            'start_date': now().date(),
            'end_date': now().date(),
            'growth_medium': 'Medium 1',
            'results': 'Growth observed',
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class CultivationPlanningAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/cultivation_planning/'

        self.strain = Strains.objects.create(
            UIN='N876',
            name='Strain CD',
            pedigree='sdfg',
            mutations='dfg',
            transformations='none',
            creation_date=now().date(),
            created_by=self.user
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_ID': strain.id,
            'planning_date': now().date(),
            'completion_date': now().date(),
            'growth_medium': 'Medium 1',
            'status': 'Planned',
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class ProjectsAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/projects/'

    def api_methods(self, user: CustomUser, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'project_name': 'New Project',
            'start_date': now().date(),
            'end_date': now().date(),
            'results': 'Successful',
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )


class CulturesAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/cultures/'

        self.project = Projects.objects.create(
            project_name='Project 1',
            start_date=now().date(),
            end_date=now().date(),
            results='Successful',
            created_by=self.user
        )

    def api_methods(self, user: CustomUser, project: Projects, token: Token, post_exp: int, put_exp: int, delete_exp: int): # type: ignore
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'project_id': project.id,
            'planning_date': now().date(),
            'results': 'Positive',
            'created_by': user.id
        }

        # POST
        response = self.client.post(self.url, creation_attrs, format='json')
        self.assertEqual(response.status_code, post_exp)
        
        if response.status_code == status.HTTP_201_CREATED:
            self.created_id = response.data['id']
            instance_url = f'{self.url}{self.created_id}/'

            # GET instance
            get_response = self.client.get(instance_url)
            self.assertEqual(get_response.status_code, status.HTTP_200_OK)

            # PUT
            put_response = self.client.put(instance_url, creation_attrs, format='json')
            self.assertEqual(put_response.status_code, put_exp)

            # DELETE
            delete_response = self.client.delete(instance_url)
            self.assertEqual(delete_response.status_code, delete_exp)

            # OPTIONS instance
            options_response = self.client.options(instance_url)
            self.assertEqual(options_response.status_code, status.HTTP_200_OK)

        # GET all
        get_all_response = self.client.get(self.url)
        self.assertEqual(get_all_response.status_code, status.HTTP_200_OK)

        # HEAD all
        head_all_response = self.client.head(self.url)
        self.assertEqual(head_all_response.status_code, status.HTTP_200_OK)

        # OPTIONS all
        options_all_response = self.client.options(self.url)
        self.assertEqual(options_all_response.status_code, status.HTTP_200_OK)

    def test_superuser(self):
        self.api_methods(
            self.superuser, self.project, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
        )

    def test_user(self):
        self.api_methods(
            self.user, self.project, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
        )