from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company, BuildingType, Place
from app.core.services.builders.agent_builder import AgentBuilder
from app.core.services.builders.product_builder import ProductBuilder


class ProductProcessBuilderTestCase(TestCase):
    def setUp(self):
        self.load_data()
        self.land: Landscape = Landscape.objects.create_land()
        self.user: User = User.objects.create_user('johnyTest', 'john@example.com', 'johnpassword')
        self.company: Company = Company.objects.create_company('johnCompany', self.user)
        self.company.balance = self.land.buy_cost
        self.land.purchase_landscape(self.company)

    def load_data(self):
        Land.objects.load_land('csv_data/landData.csv')
        BuildingType.objects.load_building_type('csv_data/buildingType.csv')
        Place.objects.load_data('csv_data/place.csv')

    def hire_agents(self):
        builder: AgentBuilder = AgentBuilder(use_generator=False)
        builder.name = 'testJohny'
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        agent = builder.build()
        self.company.hire(agent)
        self.assertEqual(agent.company_name, self.company.company_name)
    
    def test_product_process_builder(self):
        pass