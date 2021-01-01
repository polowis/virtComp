from app.models.core.agent import AgentCustomer, AgentStats
from ..citizen.name_generator import NameGenerator
from app.models.constants import Land
import math
import random


class AgentBuilder(object):
    """The agent builder class. Responsible for constructing agents"""
    def __init__(self):
        self.generator = NameGenerator.load()
        self._name = None
        self._continent = None
        self._city = None

    def build(self):
        """Build Agent. Return AgentCustomer instance"""
        name_generator_loader = NameGenerator.load()
        agent: AgentCustomer = AgentCustomer.objects.create_agent(
            name=name_generator_loader.generate_word())
        AgentStats.attribute.create_stats(agent)
        return agent

    
    @property
    def name(self) -> str:
        return self._name or self.generate_agent_name()
    
    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self._name = value
        raise TypeError("Name must be a string but got %s" % type(value))

    @property
    def continent(self):
        return self._continent or self.generate_random_continent()
    
    @continent.setter
    def continent(self, value):
        if isinstance(value, str):
            self._continent = value
        raise TypeError("Continent must be a string but got %s" % type(value))
    
    def generate_random_continent(self):
        """Generate random continent"""
        supported_continent = Land.objects.get_supported_continents()
        return supported_continent[math.floor(random.random * len(supported_continent))]
    
    def generate_agent_name(self):
        return self.generator.generate_word(1)[0]