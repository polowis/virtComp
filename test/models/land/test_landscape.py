from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company
from django.utils import timezone
import datetime


class LandscapeTestCase(TestCase):
    def setUp(self):
        Land.objects.load_land('csv_data/landData.csv')
        self.land: Landscape = Landscape.objects.create_land('asia')
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user, 'asia')
    
    def test_bulk_create_landscape(self):
        Landscape.objects.create_multiple_landscape('europe', 10)

    def test_land_manager_is_available(self):
        land_is_available = Landscape.objects.landscape_is_available(self.land.land_id)
        self.assertEqual(land_is_available, True)
    
    def test_land_manager_is_available_with_force_index(self):
        land_is_available = Landscape.objects.landscape_is_available(self.land.id, force_primary=True)
        self.assertEqual(land_is_available, True)
    
    def test_get_landscape_by_id(self):
        test_land = Landscape.objects.get_landscape_by_id(self.land.land_id)
        self.assertEqual(self.land.land_id, test_land.land_id)

    def test_land_is_created(self):
        self.assertEqual(self.land.continent, 'asia')
    
    def test_land_able_to_buy(self):
        self.assertEqual(self.land.can_be_purchased(), True)
    
    def test_land_not_able_to_buy_by_company(self):
        self.company.balance = self.land.buy_cost - 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'buy_cost'), False)
    
    def test_land_not_able_to_buy_by_company_without_cost_key(self):
        self.company.balance = self.land.buy_cost - 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'buy'), False)
    
    def test_land_not_able_to_buy_by_company_without_cost_key_upper(self):
        self.company.balance = self.land.buy_cost - 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'BUY'), False)
    
    def test_land_able_to_buy_by_company(self):
        self.company.balance = self.land.buy_cost + 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'buy_cost'), True)
    
    def test_land_able_to_rent_by_company(self):
        self.company.balance = self.land.rent_cost + 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'rent_cost'), True)
    
    def test_land_not_able_to_rent_by_company(self):
        self.company.balance = self.land.rent_cost - 1
        self.assertEqual(self.land.company_able_to_purchase(self.company, 'rent_cost'), False)
    
    def test_company_required_extra_cost_to_buy_landscape(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEqual(extra_cost_land.required_extra_continent_cost(self.company), True)

    def test_extra_continent_buy_cost_normal_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEqual(
            extra_cost_land.get_extra_contient_cost(self.company, 'continent_cost'), extra_cost_land.continent_cost
        )
    
    def test_extra_continent_buy_cost_uppercased(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEqual(
            extra_cost_land.get_extra_contient_cost(self.company, 'CONTINENT_COST'), extra_cost_land.continent_cost
        )
    
    def test_landscape_does_not_required_extra_continent_cost(self):
        self.assertEqual(self.land.get_extra_contient_cost(self.company, 'continent_cost'), 0)
    
    def test_extra_continent_rent_cost_normal_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEqual(
            extra_cost_land.get_extra_contient_cost(self.company, 'continent_rent'), extra_cost_land.continent_rent
        )
    
    def test_extra_continent_rent_cost_upper_case(self):
        extra_cost_land = Landscape.objects.create_land('europe')
        self.assertEqual(
            extra_cost_land.get_extra_contient_cost(self.company, 'CONTINENT_RENT'), extra_cost_land.continent_rent
        )

    def test_landscape_is_bought(self):
        self.assertEqual(self.land.already_bought(), False)
    
    def test_buy_landscape(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        self.assertEqual(self.company.balance, 1)
        self.assertEqual(self.land.already_bought(), True)

    def test_own_by_landscape_string(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        self.assertEqual(self.land.owned_by(self.company.company_name), True)
    
    def test_own_by_landscape_object(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        self.assertEqual(self.land.owned_by(self.company), True)

    def test_get_landscape_after_own(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        test_land = Landscape.objects.get_single_landscape_by_company(self.land.land_id, self.company)
        self.assertEqual(self.land.land_id, test_land.land_id)
    
    def test_company_buy_landscape_backward(self):
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.buy_cost
        if land.can_be_purchased():
            if self.company.can_own_landscape(land, 'buy'):
                self.company.purchase_landscape(land)
                self.assertEqual(land.company_name, self.company.company_name)
                self.assertEqual(self.company.balance, 0)
    
    def test_company_buy_landscape_backward_with_upper_keyword(self):
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.buy_cost
        if land.can_be_purchased():
            if self.company.can_own_landscape(land, 'BUY'):
                self.company.purchase_landscape(land)
                self.assertEqual(land.company_name, self.company.company_name)
                self.assertEqual(self.company.balance, 0)

    def test_company_rent_landscape(self):
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.rent_cost
        land.rent_landscape(self.company)
        self.assertEqual(land.owned_by(self.company), True)
    
    def test_company_needs_to_pay_rent(self):
        now = timezone.now() - datetime.timedelta(days=8)
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.rent_cost
        land.rent_landscape(self.company)
        land.last_collected_money_at = now
        self.assertEqual(land.needs_to_pay_rent(), True)
    
    def test_company_needs_to_pay_rent_false(self):
        now = timezone.now() - datetime.timedelta(days=6)
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.rent_cost
        land.rent_landscape(self.company)
        land.last_collected_money_at = now
        self.assertEqual(land.needs_to_pay_rent(), False)
    
    def test_company_needs_to_pay_rent_on_due(self):
        now = timezone.now() - datetime.timedelta(days=7)
        land = Landscape.objects.create_land('asia')
        self.company.balance = land.rent_cost
        land.rent_landscape(self.company)
        land.last_collected_money_at = now
        self.assertEqual(land.needs_to_pay_rent(), True)


    


