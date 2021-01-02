from django.db import models


class ContinentManager(models.Manager):
    def get_continent_list(self):
        pass


class Continent(models.Model):
    name = models.CharField(max_length=255)
    gdp_capita = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    cpi = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    inflation_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    objects = ContinentManager()