from django.db import models

class CompanyType(models.Model):
    field = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=20, decimal_places=4)
    can_sell = models.BooleanField(default=False)
    storage = models.IntegerField()

