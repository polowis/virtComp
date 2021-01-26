from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Landscape, Land, Company, BuildingType, Place
from app.core.services.builders.agent_builder import AgentBuilder
from app.core.services.builders.building_builder import BuildingBuilder


class CompanyAgent(TestCase):
    """This test case refers to anything related between a company and its agents"""
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

    def test_hire_an_agent(self):
        agent = self.create_agent()
        self.company.hire(agent)
        self.assertEqual(agent.company_name, self.company.company_name)
    
    def purchase_building(self):
        mine: BuildingType = BuildingType.objects.get_building_by_type('supreme mine')
        self.company.balance = mine.get_buy_cost()
        building = BuildingBuilder.construct(mine.name, 'myfirstbuilding', self.company,
                                             'buy', 0, self.land)
        return building
    
    def create_agent(self):
        builder: AgentBuilder = AgentBuilder(use_generator=False)
        builder.name = 'testJohny'
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        return builder.build()

    def test_distribute_agent_after_hiring(self):
        building = self.purchase_building()
        agent = self.create_agent()
        self.company.hire(agent)
        self.company.distribute(agent, building)

        self.assertEqual(agent.building, building)
