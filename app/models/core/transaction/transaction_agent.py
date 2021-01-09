from django.db import models
from django.utils import timezone
import datetime
from app.models.core import Company
from app.models.core.agent import AgentCustomer


class AgentTransactionManager(models.Manager):
    def get_total_income(self, continent: str, start=None, end=None):
        start = start or timezone.now() - datetime.timedelta(days=7)
        end = end or timezone.now()
        return self.filter(created_at__range=[start, end], continent=continent)
    
    def create_transaction(self, agent: AgentCustomer, company: Company):
        """Create transaction object from an agent purchases product from company instance"""
        self.create(agent_id=agent.agent_id, agent=agent)
        pass


class AgentTransaction(models.Model):
    """The Agent transaction model to deal with anything related to Transaction"""
    payment_id = models.IntegerField()
    customer_id = models.IntegerField()
    agent = models.ForeignKey(AgentCustomer, on_delete=models.CASCADE)
    producer_id = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    continent = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(editable=False)

    objects = AgentTransactionManager()


