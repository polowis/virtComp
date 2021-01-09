from django.db import models
from app.models.core.agent import AgentCustomer
from django.utils import timezone


class ContinentManager(models.Manager):
    def get_continent_list(self):
        pass
    
    def get_gdp_per_capita(self, continent_name: str) -> float:
        """Return the average salary """
        return AgentCustomer.objects.get_average_salary(continent_name)


class Continent(models.Model):
    name = models.CharField(max_length=255)
    gdp_capita = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    cpi = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    inflation_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    update_at = models.DateTimeField(null=True)

    objects = ContinentManager()

    def save(self, *args, **kwargs):
        self.update_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def update_cpi(self, new_cpi):
        self.cpi = new_cpi
        self.save()