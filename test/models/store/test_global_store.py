from django.test import TestCase
from app.models import User, Company, GlobalStore


class GlobalStoreModelTestCase(TestCase):
    def setUp(self):
        self.create_user()
        
    def create_user(self):
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user)
    
    def test_register_company_to_global_store(self):
        store: GlobalStore = GlobalStore.objects.register(company=self.company)
        self.assertEqual(store.company_name, self.company.company_name)