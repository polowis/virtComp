from django.test import TestCase, Client


class StaticPageTest(TestCase):
    def setUp(self):
        #  defines the client for testing purpose
        self.client = Client()
    
    def test_default_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)