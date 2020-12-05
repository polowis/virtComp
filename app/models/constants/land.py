from django.db import models

class Land(models.Model):
    level = models.IntegerField()
    cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent = models.DecimalField(max_digits=20, decimal_places=4)
    max_land_cost = models.DecimalField(max_digits=20, decimal_places=4)
    min_land_cost = models.DecimalField(max_digits=20, decimal_places=4)
