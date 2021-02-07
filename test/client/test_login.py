from django.test import TestCase, Client
from app.models import User


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'example@example.com', 'mypassword')
    
    def test_view_login_page_if_anonymous(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
    
    def test_login_user(self):
        response = self.client.login(username='john', password='mypassword')
        self.assertEqual(True, response)
    
    def test_failed_login(self):
        response = self.client.login(username='john', password='wrongpass')
        self.assertEqual(False, response)