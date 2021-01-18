from app.models.constants import Item
from app.models.core.product import ProductProducing, AgentProducing
from app.models.core import Building
from typing import List
from app.models.core.agent import AgentCustomer


class ProductBuilder(object):
    """
    Product builder class. It will not create a product but instead creating a process which later will be used to
    creeate final product

    This should pass owner validation first before calling this class as it will not check for owner validity
    """
    def __init__(self, item: Item = None, building: Building = None, agents: List[AgentCustomer] = None):
        """
        Item: The item instance (this should be the constant item not the produced item)
        Building: The building instance this item should be produced at
        Agent: list of agents that should be building this product

        
        """
        self.agents: List[AgentCustomer] = agents or []
        self.item: Item = item
        self.building: Building = building
        self.producing_time = self.get_producing_time(self.item.time_to_produce)
    
    def set_item(self, item: Item):
        """Set the item"""
        if isinstance(item, Item):
            self.item = item
            return self
        elif isinstance(item, str):
            item = self._get_item_instance(item)
            if self.item is None:
                raise TypeError('Item must be a valid name')
            self.item = item
            return self
        raise TypeError("item must be an instance of Item but got %s" % type(item))

    def set_building(self, building: Building):
        """Set the building"""
        if isinstance(building, Building):
            self.building = building
            return self
        raise TypeError("building must be an instance of Building but got %s" % type(building))

    def produce_item(self):
        """Handle produce item process. The item must be valid and
        cannot be none. Update

        raise ValueError exception if the item is not valid
        """
        if isinstance(self.item, Item) and self.is_valid():
            product_process = ProductProducing.objects.create_proccess(
                item=self.item,
                expected_quality=self.item.raw_quality,
                time=self.producing_time
            )
            for agent in self.agents:
                AgentProducing.objects.create_producing_agent(agent=agent, process=product_process)
            self.update_worker_status()
            return product_process
        else:
            item = self._get_item_instance(self.item)
            if item is None:
                raise ValueError('Item Cannot be none')
            
    
    def _get_item_instance(self, item_name):
        try:
            item = Item.objects.get(name=item_name)
            return item
        except Item.DoesNotExist:
            return None
        
    def building_can_produce(self, building: Building, item: Item):
        """Return true if the building can produce the item"""
        pass
    
    def continent_can_produce(self, continent: str, item: Item):
        pass


    def get_producing_time(self, base_time):
        """Return the expected time to produce from this given agent(s)"""
        qualification_score = self.get_average_agents_qualification()
        productivity_score = self.get_average_agents_productivity()
        total_score = qualification_score + productivity_score
        time_score = (qualification_score * 1 * 3 * productivity_score * 2) / total_score
        return self.item.time_to_produce - (time_score / self.item.time_to_produce * 10)
    
    def get_expected_quality(self):
        pass
    
    def add_agent(self, agent):
        """Add agent to the production chain"""
        if isinstance(agent, AgentCustomer):
            self.agents.append(agent)
            return self
        raise TypeError("Agent must be an instance of AgentCustomer but got %s" % type(agent))
        
    
    def get_average_agents_qualification(self):
        """Return the average qualification of agents in the given cohort"""
        return sum([agent.agentstats.qualification for agent in self.agents]) / len(self.agents)
    
    def get_average_agents_productivity(self):
        """Return the average productivity of agents in the given cohort"""
        return sum([agent.agentstats.productivity for agent in self.agents]) / len(self.agents)
    
    def update_worker_status(self, status=True) -> None:
        """Set the worker status. If the given status is true, the worker
        will be set to is_producing, false otherwise.

        This method will call bulk_update to update the status of worker

        You will need to call this method again after finished producing.
        """
        for agent in self.agents:
            agent.is_producing = True
        AgentCustomer.objetcs.bulk_update(self.agents, ['is_producing'])
    
    def is_valid(self):
        """Return true if isvald to produce"""
        return self.building.can_produce(self.item) and self.agents_are_free_to_produce()
    
    def agents_are_free_to_produce(self):
        """Return true if all agents in the collection are able to produce
        The not working status must be true
        """
        for agent in self.agents:
            if agent.is_producing is True:
                return False
        return True
        