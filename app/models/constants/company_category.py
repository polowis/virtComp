from django.db import models

class CompanyCategory(models.Model):
    category = models.CharField(max_length=255)
    building_cost = models.DecimalField(max_digits=20, decimal_places=4)
    building_rent = models.DecimalField(max_digits=20, decimal_places=4)
    upgrade_cost = models.DecimalField(max_digits=20, decimal_places=4)
    upgrade_cost_growth = models.DecimalField(max_digits=20, decimal_places=4)
    max_employees = models.BigIntegerField()
    max_employees_growth = models.DecimalField(max_digits=20, decimal=4)
    max_storage = models.BigIntegerField()
    max_storage_growth = models.DecimalField(max_digits=20, decimal=4)