from __future__ import annotations
from django.db import models
from django.utils import timezone
from app.core.util.base import generate_unique_id
from django.db.models import Avg


class AgentManager(models.Manager):
    def create_agent(self, values) -> AgentCustomer:
        """create agent customer"""
        agent = self.create(**values)
        return agent
    
    def get_average_salary(self, continent: str):
        """Return the average salary of the given continent"""
        return self.filter(continent=continent).aggregate(Avg('salary'))


class AgentCustomer(models.Model):
    agent_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    continent = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    hour_of_work_per_day = models.IntegerField(default=0)

    is_rest = models.BooleanField(default=True)
    is_employed = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    objects = AgentManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)