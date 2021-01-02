from django.db import models
from app.models.core.agent import AgentCustomer
from django.utils import timezone


class AgentStatsTrackerManager(models.Manager):
    def create_tracker(self, values):
        tracker = self.create(**values)
        return tracker


class AgentStatsTracker(models.Model):
    agent = models.ForeignKey(AgentCustomer, on_delete=models.CASCADE)
    qualification = models.IntegerField()
    productivity = models.IntegerField()
    communication = models.IntegerField()
    creativity = models.IntegerField()
    leadership = models.IntegerField()
    learning = models.IntegerField()

    objects = AgentStatsTrackerManager()

    created_at = models.DateTimeField(default=timezone.now)