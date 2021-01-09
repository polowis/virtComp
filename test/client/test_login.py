from django.test import TestCase, Client


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_view_login_page_if_anonymous(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)