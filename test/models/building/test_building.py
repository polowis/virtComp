from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company, Building, BuildingType
from app.models.core.exception import UnableToConstructBuilding


class BuildingPurchasingTestCase(TestCase):
    def setUp(self):
        Land.objects.load_land('csv_data/landData.csv')
        BuildingType.objects.load_building_type('csv_data/buildingType.csv')
        self.land: Landscape = Landscape.objects.create_land('asia')
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user, 'asia')
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
    
    def test_buy_building(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        
        self.assertEqual(building.building_name, 'myfirstbuilding')
    
    def test_buy_building_with_higher_level_than_0(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost(1)
        with self.assertRaises(UnableToConstructBuilding):
            Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                             'buy', 1, self.land)
        
    
    def test_buy_building_is_buy_status(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        
        self.assertEqual(building.is_buy, True)
    
    def test_buy_building_is_rent_status(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        
        self.assertEqual(building.is_rent, False)
    
    
    def test_building_belong_to(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        self.assertEqual(building.belongs_to(self.land), True)
    
    def test_not_belongs_to(self):
        test_land = Landscape.objects.create_land('asia')
        self.company.balance = test_land.buy_cost + 1
        test_land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, test_land)
        self.assertEqual(building.belongs_to(self.land), False)
    
    def test_building_own_by(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('restaurant')
        self.company.balance = restaurant.get_buy_cost()
        building = Building.objects.create_building("restaurant", 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        
        self.assertEqual(building.owned_by(self.company), True)
    
    def test_rent_building_at_0(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(0)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', 0, self.land)
        
        self.assertEqual(building.building_name, 'mymarket')
    
    def test_rent_building_at_equal_land_level(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        market: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = market.get_rent_cost(self.land.level)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', self.land.level, self.land)
        
        self.assertEqual(building.building_name, 'mymarket')
    
    def test_rent_building_at_higher_level_than_land(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(self.land.level + 1)
        with self.assertRaises(UnableToConstructBuilding):
            Building.objects.create_building("market", 'mymarket', self.company,
                                             'rent', self.land.level + 1, self.land)
    
    def test_rent_building_at_negative_level_than_land(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(-1)
        with self.assertRaises(UnableToConstructBuilding):
            Building.objects.create_building("market", 'mymarket', self.company,
                                             'rent', -1, self.land)
    
    def test_rent_building_belongs_to(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(0)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', 0, self.land)
        
        self.assertEqual(building.belongs_to(self.land), True)
    
    def test_rent_building_owned_by(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(0)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', 0, self.land)
        
        self.assertEqual(building.owned_by(self.company), True)
    
    def test_rent_building_is_rent_status(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(0)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', 0, self.land)
        
        self.assertEqual(building.is_rent, True)
    
    def test_rent_building_is_buy_status(self):
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        restaurant: BuildingType = BuildingType.objects.get_building_by_type('market')
        self.company.balance = restaurant.get_rent_cost(0)
        building = Building.objects.create_building("market", 'mymarket', self.company,
                                                    'rent', 0, self.land)
        
        self.assertEqual(building.is_buy, False)
        