from __future__ import annotations
from django.db import models
from django.utils import timezone


class AgentCustomer(models.Model):
    agent_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    company_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)