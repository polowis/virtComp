from app.models.core.agent import AgentCustomer, AgentStats
from ..citizen.name_generator import NameGenerator


class AgentBuilder(object):
    def __init__(self):
        self.generator = NameGenerator.load()
        self._name = self.generator.generate_word(1)[0]
        pass

    def build(self):
        name_generator_loader = NameGenerator.load()
        agent: AgentCustomer = AgentCustomer.objects.create_agent(
            name=name_generator_loader.generate_word())
        agent_stats = AgentStats.attribute.create_stats(agent)
        
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self.name = value
        raise TypeError("Name must be a string but got %s" % type(value))