from django.db import models


class AgentTransaction(models.Model):
    """The Agent transaction model to deal with anything related to Transaction"""
    payment_id = models.IntegerField()
    agent_id = models.IntegerField()
    agent = models.ForeignKey()
    company_id = models.CharField(max_length=255)
    company = models.ForeignKey()
    total = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(editable=False)


