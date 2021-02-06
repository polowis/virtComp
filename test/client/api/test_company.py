from django.test import TestCase, Client
from app.models import User


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
    
    def test_failed_create_company(self):
        response = self.client.post(self.api_endpoint, {'companyName': '?dfloe^&', 'continent': 'alantica'})
        self.assertEqual(response.json()['error'], True)
    
