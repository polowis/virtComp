from django.test import TestCase, Client
from app.models import User, Company, Landscape


class LandscapeTestCase(TestCase):

    api_endpoint = '/api/v1/landscape/'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
        self.client.login(username='john', password='mypassword')
        self.land: Landscape = Landscape.objects.create_land()
    
    def sign_in_company(self):
        Company.objects.create_company('johnCompany', self.user, 'alantica')
        self.client.post('/api/v1/user/company/sign', {'companyName': 'johnCompany'})