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
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'buy_cost'), False)
    
    def test_land_not_able_to_buy_by_company_without_cost_key(self):
        self.company.balance = self.land.buy_cost - 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'buy'), False)
    
    def test_land_not_able_to_buy_by_company_without_cost_key_upper(self):
        self.company.balance = self.land.buy_cost - 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'BUY'), False)
    
    def test_land_able_to_buy_by_company(self):
        self.company.balance = self.land.buy_cost + 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'buy_cost'), True)
    
    def test_land_able_to_rent_by_company(self):
        self.company.balance = self.land.rent_cost + 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'rent_cost'), True)
    
    def test_land_not_able_to_rent_by_company(self):
        self.company.balance = self.land.rent_cost - 1
        self.company.save()
        self.assertEquals(self.land.company_able_to_purchase(self.company, 'rent_cost'), False)
    
    def test_company_required_extra_cost_to_buy_landscape(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEquals(extra_cost_land.required_extra_continent_cost(self.company), True)

    def test_extra_continent_buy_cost_normal_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEquals(
            extra_cost_land.get_extra_contient_cost(self.company, 'continent_cost'), extra_cost_land.continent_cost
        )
    
    def test_extra_continent_buy_cost_uppercased(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEquals(
            extra_cost_land.get_extra_contient_cost(self.company, 'CONTINENT_COST'), extra_cost_land.continent_cost
        )
    
    def test_landscape_does_not_required_extra_continent_cost(self):
        self.assertEquals(self.land.get_extra_contient_cost(self.company, 'continent_cost'), 0)
    
    def test_extra_continent_rent_cost_normal_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEquals(
            extra_cost_land.get_extra_contient_cost(self.company, 'continent_rent'), extra_cost_land.continent_rent
        )
    
    def test_extra_continent_rent_cost_upper_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEquals(
            extra_cost_land.get_extra_contient_cost(self.company, 'CONTINENT_RENT'), extra_cost_land.continent_rent
        )

    def test_landscape_is_bought(self):
        self.assertEquals(self.land.already_bought(), False)
    
    def test_buy_landscape(self):
        self.company.balance = self.land.buy_cost + 1
        self.company.save()
        self.land.purchase_landscape(self.company)
        self.assertEquals(self.company.balance, 1)
        self.assertEquals(self.land.already_bought(), True)
    


