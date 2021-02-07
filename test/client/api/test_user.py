from django.test import TestCase, Client
from app.models import User, Company


class UserAPITestCase(TestCase):

    api_endpoint = '/api/v1/user/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
        self.client.login(username='john', password='mypassword')
    
    def test_current_user(self):
        response = self.client.get(self.api_endpoint)
        self.assertEqual(response.json()['username'], 'john')
        self.assertEqual(response.json()['email'], 'example@example.com')
    
    def test_get_all_company_belong_to_user(self):
        Company.objects.create_company('johnCompany', self.user, 'alantica')
        response = self.client.get(self.api_endpoint + 'company/')
        self.assertEqual(response.json()[0]['company_name'], 'johnCompany')
    
    def test_sign_company(self):
        Company.objects.create_company('johnCompany', self.user, 'alantica')
        response = self.client.post(self.api_endpoint + 'company/sign/', {'companyName': 'johnCompany'})
        self.assertEqual(response.json()['error'], False)
    
    def test_valid_user(self):
        response = self.client.post(self.api_endpoint + 'valid/', {'username': 'alice', 'email': 'alice@gmail.com'})
        self.assertEqual(response.json()['error'], False)
    
    def test_valid_user_with_no_email(self):
        response = self.client.post(self.api_endpoint + 'valid/', {'username': 'alice'})
        self.assertEqual(response.json()['error'], True)

    def test_valid_user_with_no_username(self):
        response = self.client.post(self.api_endpoint + 'valid/', {'email': 'alice@gmail.com'})
        self.assertEqual(response.json()['error'], True)
    
    def test_valid_user_with_no_param(self):
        response = self.client.post(self.api_endpoint + 'valid/')
        self.assertEqual(response.json()['error'], True)
    
    def test_valid_user_with_invalid_email(self):
        response = self.client.post(self.api_endpoint + 'valid/', {'username': 'alice', 'email': 'alice'})
        self.assertEqual(response.json()['error'], True)

