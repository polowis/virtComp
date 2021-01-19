from __future__ import annotations
from django.db import models
from app.models.constants import Item
from ..building import Building
from django.utils import timezone
import datetime
import random
from ..agent.agent import AgentCustomer


class ProductProducingManager(models.Manager):
    """The producing process manager"""
    def create_proccess(self, item: Item, expected_quality: float, time: int):
        """Create the producing process for the given item"""
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(seconds=time)
        item_name = item.name
        self.create(name=item_name, item=item, expected_quality=expected_quality, start_time=start_time,
                    end_time=end_time)


class ProductProducing(models.Model):
    """Product producing process"""
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    # the building where the process started
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    # the is_success field will be updated as soon as the time is finished
    is_success = models.BooleanField(null=True)
    is_completed = models.BooleanField(null=True)
    expected_quality = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = ProductProducingManager()

    def is_finished(self):
        """Check if the product has finished. Doing this will also try to
        update the process
        """
        if not self.is_completed:
            self.is_completed = timezone.now() > self.end_time
        return self.is_completed
    
    def move_to(self, building):
        """This function will be used to move the item into storage after
        finishing
        """
        pass

    def update_success(self) -> None:
        if self.is_success is None:
            success_score = random.randint(1, 100)
            self.is_success = success_score < self.item.prob_per_attempt
            self.update_agents()
        return
    
    def update_agents(self):
        processes = AgentProducing.objects.filter(process_id=self.id)
        for process in processes:
            process.agent.is_producing = False
            process.agent.save()


class AgentProducingManager(models.Manager):
    def create_producing_agent(self, agent=AgentCustomer, process=ProductProducing):
        agent_process = self.create(agent=agent, producing_process=process, process_id=process.id)
        return agent_process


class AgentProducing(models.Model):
    """The agent produce the particular item"""
    process_id = models.IntegerField()
    agent = models.ForeignKey(AgentCustomer, on_delete=models.CASCADE)
    producing_process = models.ForeignKey(ProductProducing, on_delete=models.CASCADE)

    objects = AgentProducingManager()
