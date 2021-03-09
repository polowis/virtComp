from django.test import TestCase, Client
from app.models import User


class BuildingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
        self.client.login(username='john', password='mypassword')
        self.client.post('/api/v1/company/', {'companyName': 'myCompany', 'continent': 'alantica'})
        self.client.post('/api/v1/user/company/sign/', {'companyName': 'johnCompany'}, follow=True)