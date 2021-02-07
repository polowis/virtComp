from django.test import TestCase, Client
from app.models import User, Company


class CompanyAPITestCase(TestCase):

    api_endpoint = '/api/v1/company/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
        self.client.login(username='john', password='mypassword')
    
    def test_create_company(self):
        response = self.client.post(self.api_endpoint, {'companyName': 'myCompany', 'continent': 'alantica'})
        self.assertEqual(response.json()['error'], False)
        self.assertEqual(response.json()['message'], 'sucessfully created')
    
    def test_failed_create_company_with_non_ascii_letters(self):
        response = self.client.post(self.api_endpoint, {'companyName': '?dfloe^&', 'continent': 'alantica'})
        self.assertEqual(response.json()['error'], True)
    
    def test_failed_create_company_with_exists_name(self):
        Company.objects.create_company('myCompany', self.user, 'alantica')
        response = self.client.post(self.api_endpoint, {'companyName': 'myCompany', 'continent': 'alantica'})
        self.assertEqual(response.json()['error'], True)
    
    def test_failed_create_company_with_no_param(self):
        response = self.client.post(self.api_endpoint)
        self.assertEqual(response.json()['error'], True)
    
    def test_failed_create_company_with_no_missing_companyname(self):
        response = self.client.post(self.api_endpoint, {'continent': 'alantica'})
        self.assertEqual(response.json()['error'], True)
    
    def test_failed_create_company_with_not_support_continent(self):
        response = self.client.post(self.api_endpoint, {'companyName': 'myCompany', 'continent': 'mycontinent'})
        self.assertEqual(response.json()['error'], True)
