from django.test import TestCase
from app.models.core import User
from app.models import Landscape, Land, Company, BuildingType, Item, Place
from app.core.services.builders.building_builder import BuildingBuilder


class BuildingItemProducingTestCase(TestCase):
    def setUp(self):
        self.load_data()
        self.land: Landscape = Landscape.objects.create_land()
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user)
        self.company.balance = self.land.buy_cost + 1
        self.land.purchase_landscape(self.company)
        building: BuildingType = BuildingType.objects.get_building_by_type('supreme mine')
        self.company.balance = building.get_rent_cost(0)
        self.building = BuildingBuilder.construct("supreme mine", 'mymine', self.company,
                                                  'rent', 0, self.land)

    def load_data(self):
        Place.objects.load_data('csv_data/place.csv')
        Land.objects.load_land('csv_data/landData.csv')
        BuildingType.objects.load_building_type('csv_data/buildingType.csv')
        Item.objects.load_items('csv_data/item.csv')

    def test_building_can_produce(self):
        item = Item.objects.get(name='diamond')  # assuming diamond is produced from surpeme mine
        self.assertEqual(self.building.can_produce(item), True)
    