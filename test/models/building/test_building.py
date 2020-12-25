from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company


class BuildingPurchasingTestCase(TestCase):
    def setUp(self):
        Land.objects.load_land('csv_data/landData.csv')
        self.land: Landscape = Landscape.objects.create_land('asia')
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user, 'asia')
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
    
    def test_buy_building(self):
        pass