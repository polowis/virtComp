from __future__ import annotations
from django.db import models
from django.utils import timezone
from app.core.util.base import generate_unique_id


class AgentManager(models.Manager):
    def create_agent(self, values) -> AgentCustomer:
        """create agent customer"""
        agent = self.create(**values)
        return agent


class AgentCustomer(models.Model):
    agent_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    continent = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    objects = AgentManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)