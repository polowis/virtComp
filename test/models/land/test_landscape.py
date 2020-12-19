from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company


class LandscapeTestCase(TestCase):
    def setUp(self):
        Land.objects.load_land('csv_data/landData.csv')
        self.land: Landscape = Landscape.objects.create_land('asia')
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user, 'asia')
    
    def test_land_is_created(self):
        self.assertEquals(self.land.continent, 'asia')
    
    def test_land_able_to_buy(self):
        self.assertEquals(self.land.can_be_purchased(), True)
    
    def test_land_not_able_to_buy_by_company(self):
        self.company.balance = self.land.buy_cost - 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company), False)
    
    def test_land_able_to_buy_by_company(self):
        self.company.balance = self.land.buy_cost + 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company), True)
    
    def test_landscape_is_bought(self):
        self.assertEquals(self.land.already_bought(), False)
    
    def test_buy_landscape(self):
        self.company.balance = self.land.buy_cost + 1
        self.company.save()
        self.land.purchase_landscape(self.company)
        self.assertEquals(self.company.balance, 1)
        self.assertEquals(self.land.already_bought(), True)
    


