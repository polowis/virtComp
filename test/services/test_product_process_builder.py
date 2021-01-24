from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company, BuildingType, Place, Item, Building
from app.core.services.builders.agent_builder import AgentBuilder
from app.core.services.builders.product_builder import ProductBuilder
from django.utils import timezone
import datetime


class ProductProcessBuilderTestCase(TestCase):
    def setUp(self):
        self.load_data()
        self.land: Landscape = Landscape.objects.create_land()
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user)
        self.company.balance = self.land.buy_cost
        self.land.purchase_landscape(self.company)
        self.building = self.purchase_building()
        self.item = self.get_sample_item()
    
    def purchase_building(self):
        mine: BuildingType = BuildingType.objects.get_building_by_type('supreme mine')
        self.company.balance = mine.get_buy_cost()
        building = Building.objects.create_building(mine.name, 'myfirstbuilding', self.company,
                                                    'buy', 0, self.land)
        return building

    def get_sample_item(self):
        return Item.objects.get(name='limestone')

    def load_data(self):
        Land.objects.load_land('csv_data/landData.csv')
        BuildingType.objects.load_building_type('csv_data/buildingType.csv')
        Place.objects.load_data('csv_data/place.csv')
        Item.objects.load_items('csv_data/item.csv')

    def hire_agents(self):
        builder: AgentBuilder = AgentBuilder(use_generator=False)
        builder.name = 'testJohny'
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        agent = builder.build()
        self.company.hire(agent)

    def hire_many_agents(self):
        builder = AgentBuilder(use_generator=False)
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        agents = builder.build_many_agents(2, ['alice', 'bob'])
        for agent in agents:
            self.company.hire(agent)
        return agents
    
    def test_product_process_builder(self):
        agents = self.hire_many_agents()
        product_builder = ProductBuilder()
        product_builder.item = self.item
        product_builder.building = self.building
        product_builder.agents = agents
        process = product_builder.produce_item()
        self.assertEqual(process.name, self.item.name)

    def test_process_complete(self):
        agents = self.hire_many_agents()
        product_builder = ProductBuilder()
        product_builder.item = 'limestone'
        product_builder.building = self.building
        product_builder.agents = agents
        process = product_builder.produce_item()
        time = timezone.now() + datetime.timedelta(seconds=self.item.raw_producing_time)
        self.assertEqual(process.is_finished(time), True)
    
    def test_process_not_complete(self):
        agents = self.hire_many_agents()
        product_builder = ProductBuilder()
        product_builder.item = 'limestone'
        product_builder.building = self.building
        product_builder.agents = agents
        process = product_builder.produce_item()
        time = process.end_time - datetime.timedelta(seconds=round(self.item.raw_producing_time / 2))
        self.assertEqual(process.is_finished(time), False)

        
