from app.models.core.agent import AgentCustomer, AgentStats
from ..citizen.name_generator import NameGenerator
from app.models.constants import Land, Place
import math
import random


class AgentBuilder(object):
    """The agent builder class. Responsible for constructing agents
    
    Please do not use AgentCustomer.objects.create_agent() as this method does not
    do any validity check but only save to the database
    """
    def __init__(self, **kwargs):
        self.generator = NameGenerator.load()
        self.generator._debug = False
        self._name = kwargs.get('name', None)
        self._continent = kwargs.get('continent', None)
        self._place = kwargs.get('place', None)
        self._age = kwargs.get('age', None)
        self.debug = True

    def build(self):
        """Build Agent. Return AgentCustomer instance"""
        if self.has_correct_location():
            agent: AgentCustomer = AgentCustomer.objects.create_agent(
                self.attribute_as_dict())
            AgentStats.attribute.create_stats(agent)
            if self.debug:
                print("Agent created at ", agent.__dict__)
            return agent
        raise Exception("Invalid Location. The place must be inside the specifed continent")
    
    def build_many_agents(self, number_of_agents) -> None:
        """Create many agents. This can improve performance by only load the model once
        But the continent must be specified can cannot generate on its own.
        """
        for agent in range(int(number_of_agents)):
            self.name = self.generator.generate_word(1)[0]
            self.place = Place.objects.get_random_place(self.continent)
            self.age = self.get_random_age()
            agent: AgentCustomer = AgentCustomer.objects.create_agent(
                self.attribute_as_dict())
            AgentStats.attribute.create_stats(agent)
            if self.debug:
                print("Agent created at ", agent.__dict__)
                print("Agent stats: ", agent.agentstats.__dict__)



    @property
    def name(self) -> str:
        return self._name or self.generate_agent_name()
    
    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self._name = value
        else:
            raise TypeError("Name must be a string but got %s" % type(value))

    @property
    def continent(self):
        return self._continent or self.generate_random_continent()
    
    @continent.setter
    def continent(self, value):
        if isinstance(value, str):
            self._continent = value
        else:
            raise TypeError("Continent must be a string but got %s" % type(value))
    
    @property
    def place(self):
        return self._place or Place.objects.get_random_place(self.continent)
    
    @place.setter
    def place(self, value):
        if isinstance(value, str):
            self._place = value
        else:
            raise TypeError("Place must be a string but got %s" % type(value))
    
    def generate_random_continent(self):
        """Generate random continent"""
        supported_continent = Land.objects.get_supported_continents()
        return supported_continent[math.floor(random.random * len(supported_continent))]
    
    def generate_agent_name(self):
        """Generate agent name"""
        return self.generator.generate_word(1)[0]
    
    def get_random_age(self, start: int = 15, end: int = 40) -> int:
        """return random age in given range"""
        return random.randint(start, end)
    
    @property
    def age(self):
        return self._age or self.get_random_age(15, 40)
    
    @age.setter
    def age(self, value: int):
        self._age = value
    
    def attribute_as_dict(self) -> dict:
        """Return agent attributes as a dictionary"""
        values = {
            'continent': self.continent,
            'place': self.place,
            'age': self.age,
            'name': self.name
        }

        return values
    
    def has_correct_location(self):
        """Return true if the given place is in the given continent"""
        return Place.objects.belongs_to(self.place, self.continent)