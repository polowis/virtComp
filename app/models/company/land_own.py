from django.db import models

from app.models.company import Company



class LandOwnManager(models.Manager):
    def create_land(self, level, buy_cost, rent_cost):
        land = self.create(level=level, buy_cost=buy_cost, rent_cost=rent_cost)
        return land
    
    def get_available_land(self):
        return self.filter(status='')


class LandOwn(models.Model):
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.IntegerField(default=0)
    company_name = models.CharField(max_length=255, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, default='')
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    objects = LandOwnManager()
