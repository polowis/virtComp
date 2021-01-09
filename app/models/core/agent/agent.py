from __future__ import annotations
from django.db import models
from django.utils import timezone
from app.core.util.base import generate_unique_id
from django.db.models import Avg
from app.models.core import Building


class AgentManager(models.Manager):
    def create_agent(self, values) -> AgentCustomer:
        """create agent customer"""
        agent = self.create(**values)
        return agent
    
    def get_average_salary(self, continent: str):
        """Return the average salary of the given continent"""
        return self.filter(continent=continent).aggregate(Avg('salary'))
    
    def get_not_producing_agents(self, building: Building):
        """Get the list of agents in the given building that
        are not producing any product
        """
        return self.filter(building=building, is_producing=False)


class AgentCustomer(models.Model):
    agent_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    continent = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    hour_of_work_per_day = models.IntegerField(default=0)

    is_rest = models.BooleanField(default=True)
    is_employed = models.BooleanField(default=False)
    is_producing = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    objects = AgentManager()

    def save(self, *args, **kwargs):
        """Save the object to the database"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def work_for(self, company: str, *args, **kwargs) -> None:
        """Set the company that this agent will work for
        
        """
        if self.building:  # if the building is already set then this will raise exception
            raise ValueError("The building is already set")
        else:
            self.company_name = company
            self.save()
    
    def work_at(self, building: Building, *args, **kwargs):
        """Set the building that this agent will work at.

        Make sure that the building belongs to the company

        raise exception if the building does not belong to the company
        """
        if building.company_name == self.company_name:
            self.building = building
            self.save()
        else:
            raise ValueError("Building does not belong to the company")