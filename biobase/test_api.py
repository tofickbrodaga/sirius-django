from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from biobaseapp.models import CustomUser, Strains

def create_api_test(model_class, url, creation_attrs, user):
    class ApiTest(TestCase):
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            # Create users
            cls.user = CustomUser.objects.create_user(username='user123', password='user001')
            cls.superuser = CustomUser.objects.create_superuser(username='admin123', password='admin01')

            # Create tokens for users
            cls.user_token = Token.objects.create(user=cls.user)
            cls.superuser_token = Token.objects.create(user=cls.superuser)

        def setUp(self):
            self.client = APIClient()

        def api_methods(self, user, token, post_exp, put_exp, delete_exp):
            self.client.force_authenticate(user=user, token=token)

            # Create model object
            try:
                created_obj = model_class.objects.create(**creation_attrs, created_by=user)
                instance_url = f'{url}{created_obj.id}/'
            except Exception as e:
                print("Error creating object:", e)
                raise

            # Debugging
            print("Created object:", created_obj)
            print("Instance URL:", instance_url)
            # GET all
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

            # GET instance
            self.assertEqual(self.client.get(instance_url).status_code, status.HTTP_200_OK)

            # POST
            self.assertEqual(self.client.post(url, creation_attrs).status_code, post_exp)

            # PUT
            self.assertEqual(self.client.put(instance_url, creation_attrs).status_code, put_exp)

            # DELETE
            self.assertEqual(self.client.delete(instance_url).status_code, delete_exp)

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

    return ApiTest

# Example usage
user = CustomUser.objects.get(username='md')  # Assuming 'admin123' is the username of the user who created the object
StrainsApiTest = create_api_test(Strains, '/api/strains/', {'UIN': 'UIN1', 'name': 'Strain1', 'pedigree': 'Pedigree', 'mutations': 'Mutations', 'transformations': 'Transformations', 'creation_date': '2024-05-02'}, user)