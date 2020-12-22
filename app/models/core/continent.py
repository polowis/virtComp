from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=255)
    gdp_capita = models.DecimalField(max_digits=20, decimal_places=4)
    cpi = models.DecimalField(max_digits=8, decimal_places=2)
    inflation_rate = models.DecimalField(max_digits=4, decimal_places=2)