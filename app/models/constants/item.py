from django.db import models
from app.models import BuildingType


class ItemManager(models.Manager):
    def get_items_by_continent(self, continent: str):
        return self.filter(continent=continent)


class Item(models.Model):
    name = models.CharField(max_length=255)
    time_to_produce = models.IntegerField()
    cost_attempt = models.DecimalField(max_digits=20, decimal_places=4)
    probability_per_attempt = models.FloatField()
    factory_type = models.CharField(max_length=255)
    factory = models.ForeignKey(BuildingType, on_delete=models.CASCADE)
    continent = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    electric_cost = models.DecimalField(max_digits=20, decimal_places=4)
    water_cost = models.DecimalField(max_digits=20, decimal_places=4)
    gas_cost = models.DecimalField(max_digits=20, decimal_places=4)
    quantity_upon_produced = models.IntegerField()
    unlock_at_building_level = models.IntegerField()