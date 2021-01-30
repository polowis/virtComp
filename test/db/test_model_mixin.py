from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Company


class ModelMixinTestCase(TestCase):
    """
    Testing model mixin using company model as example
    """
    def setUp(self):
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user)

    def test_is_clean(self):
        company = Company.objects.get(id=self.company.id)
        self.assertEqual(company.is_clean(), True)
    
    def test_is_clean_with_field(self):
        company = Company.objects.get(id=self.company.id)
        self.assertEqual(company.is_clean('balance'), True)
    
    def test_is_not_clean_field(self):
        company = Company.objects.get(id=self.company.id)
        company.balance = 100
        self.assertEqual(company.is_clean('balance'), False)

    def test_is_dirty(self):
        company = Company.objects.get(id=self.company.id)
        company.balance = 100
        self.assertEqual(company.is_dirty(), True)
    
    def test_is_dirty_with_field(self):
        company = Company.objects.get(id=self.company.id)
        company.balance = 100
        self.assertEqual(company.is_dirty('balance'), True)
    
    def test_is_not_dirty_field(self):
        company = Company.objects.get(id=self.company.id)
        company.balance = 100
        self.assertEqual(company.is_dirty('company_name'), False)
    
