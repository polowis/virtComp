from django.test import TestCase
from app.core.services.builders.agent_builder import AgentBuilder
from app.models.constants import Land, Place


class AgentBuilderTestCase(TestCase):
    def setUp(self):
        Place.objects.load_data('csv_data/place.csv')
        Land.objects.load_land('csv_data/landData.csv')

    def test_build_without_generator(self):
        builder: AgentBuilder = AgentBuilder(use_generator=False)
        builder.name = 'testJohny'
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        agent = builder.build()
        self.assertEqual(agent.name, 'testJohny')
    
    def test_build_many_agent_without_generator(self):
        builder: AgentBuilder = AgentBuilder(use_generator=False)
        builder.debug = False
        builder.continent = Land.objects.default_continent()
        agents = builder.build_many_agents(2, ['johny', 'alice'])
        self.assertEqual(agents[0].name, 'johny')
        self.assertEqual(agents[1].name, 'alice')

