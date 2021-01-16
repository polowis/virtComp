from __future__ import annotations
from django.db import models
import csv


class ItemLoader(object):
    def __init__(self, path):
        self.path = path
    

    def load(self):
        try:
            with open(path) as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    print(row)
        except Exception as e:
            raise Exception(e)


class ItemManager(models.Manager):
    def get_items_by_continent(self, continent: str):
        return self.filter(continent=continent)
    

    def load_items(self, path: str = './csv_data/item.csv'):
        if isinstance(path, str):
            loader = ItemLoader(path)
            loader.load()


class Item(models.Model):
    name = models.CharField(max_length=255)
    cost_attempt = models.DecimalField(max_digits=20, decimal_places=4)
    probability_per_attempt = models.DecimalField(max_digits=5, decimal_places=2)
    raw_quality = models.IntegerField()
    employees_needed = models.IntegerField()
    quantity_per_attempt = models.IntegerField()
    category_type = models.CharField(max_length=255)
    building_type = models.TextField()
    continents = models.TextField()
    unit = models.CharField(max_length=255)
    electric_cost = models.DecimalField(max_digits=20, decimal_places=4)
    water_cost = models.DecimalField(max_digits=20, decimal_places=4)
    gas_cost = models.DecimalField(max_digits=20, decimal_places=4)
    unlock_at_building_level = models.IntegerField()

    def building_to_dict(self):
        """return the dictionary contains the building type that can produce the item"""
        return str(self.building_type).split(",")
    
    def continent_to_dict(self):
        return str(self.continent).split(",")