from django.test import TestCase, Client
from app.models import User, Company, Landscape, Place, Land


class LandscapeTestCase(TestCase):

    api_endpoint = '/api/v1/landscape/'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
        self.client.login(username='john', password='mypassword')
        Place.objects.load_data('csv_data/place.csv')
        Land.objects.load_land('csv_data/landData.csv')
        self.land: Landscape = Landscape.objects.create_land()
        self.sign_in_company()
    
    def sign_in_company(self):
        Company.objects.create_company('johnCompany', self.user, 'alantica')
        self.client.post('/api/v1/user/company/sign', {'companyName': 'johnCompany'}, follow=True)
    
    def landscape_view_access(self):
        self.client.post('/api/v1/user/company/sign', {'companyName': 'johnCompany'}, follow=True)
        response = self.client.get(self.api_endpoint)
        self.assertEqual(response.status_code, 200)

