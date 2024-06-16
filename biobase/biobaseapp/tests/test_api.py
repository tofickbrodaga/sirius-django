"""Test for REST API."""
from biobaseapp.models import CustomUser, Projects, Strains
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class StrainsAPITest(APITestCase):
    """Test for REST API for strains."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/strains/'

    def api_methods(self, user: CustomUser, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """Test API methods for strains.

        Args:
            user: user instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'UIN': 'N877',
            'name': 'New Strain',
            'pedigree': 'xyz',
            'mutations': 'abc',
            'transformations': 'none',
            'creation_date': now().date(),
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class StrainProcessingAPITest(APITestCase):
    """Test suite for Strain Processing API methods."""

    def setUp(self):
        """Set up test environment."""
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
            created_by=self.user,
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """Test API methods for Strain Processing.

        Args:
            user: user instance
            strain: strain instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_id': strain.id,
            'processing_date': now().date(),
            'description': 'None',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class SubstanceIdentificationAPITest(APITestCase):
    """Test suite for Substance Identification API methods."""

    def setUp(self):
        """Set up test environment."""
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
            created_by=self.user,
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """Test API methods for substance identification.

        Args:
            user: user instance
            strain: strain instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_id': strain.id,
            'identification_date': now().date(),
            'results': 'Positive',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class ExperimentsAPITest(APITestCase):
    """Test Experiments API methods for superuser and user."""

    def setUp(self):
        """Set up the test environment for the Experiments API test case."""
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
            created_by=self.user,
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """
        Test API methods for superuser and user.

        Args:
            user: user instance
            strain: strain instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_UIN': strain.id,
            'start_date': now().date(),
            'end_date': now().date(),
            'growth_medium': 'Medium 1',
            'results': 'Growth observed',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class CultivationPlanningAPITest(APITestCase):
    """Test the Cultivation Planning API methods."""

    def setUp(self):
        """Set up the test environment for the Cultivation Planning API test case."""
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
            created_by=self.user,
        )

    def api_methods(self, user: CustomUser, strain: Strains, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """
        Test API methods for user and superuser.

        Args:
            user: user instance
            strain: strain instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'strain_ID': strain.id,
            'planning_date': now().date(),
            'completion_date': now().date(),
            'growth_medium': 'Medium 1',
            'status': 'Planned',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.strain, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.strain, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class ProjectsAPITest(APITestCase):
    """Test case for Project API methods for superuser and user."""

    def setUp(self):
        """Set up the test environment for the Projects API test case."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user', password='user')
        self.superuser = CustomUser.objects.create_superuser(username='admin', password='admin')

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.url = '/api/projects/'

    def api_methods(self, user: CustomUser, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """
        Test API methods for superuser and user.

        Args:
            user: user instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'project_name': 'New Project',
            'start_date': now().date(),
            'end_date': now().date(),
            'results': 'Successful',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )


class CulturesAPITest(APITestCase):
    """Test API methods for Cultures model."""

    def setUp(self):
        """Set up test environment."""
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
            created_by=self.user,
        )

    def api_methods(self, user: CustomUser, project: Projects, token: Token, post_exp: int,
                    put_exp: int, delete_exp: int): # type: ignore
        """Test API methods for superuser and user.

        Args:
            user: user instance
            project: project instance
            token: token instance
            post_exp: expected response code for POST method
            put_exp: expected response code for PUT method
            delete_exp: expected response code for DELETE method
        """
        self.client.force_authenticate(user=user, token=token)

        creation_attrs = {
            'project_id': project.id,
            'planning_date': now().date(),
            'results': 'Positive',
            'created_by': user.id,
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
        """Test API methods for superuser."""
        self.api_methods(
            self.superuser, self.project, self.superuser_token,
            status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT,
        )

    def test_user(self):
        """Test API methods for user."""
        self.api_methods(
            self.user, self.project, self.user_token,
            status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
        )
