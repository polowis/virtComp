from __future__ import annotations
from django.db import models
import csv


class ItemCSVRow(object):
    def __init__(self, row):
        self.row = row

    @property
    def name(self):
        return self.row[0]
    
    @property
    def cost_attempt(self):
        return self.row[1]
    
    @property
    def probability_per_attempt(self):
        return self.row[2]
    
    @property
    def raw_quality(self):
        return self.row[3]
    
    @property
    def employees_needed(self):
        return self.row[4]
    
    @property
    def quantity_per_attempt(self):
        return self.row[5]
    
    @property
    def category_type(self):
        return self.row[6]
    
    @property
    def building_type(self):
        return self.row[7]
    
    @property
    def continents(self):
        return self.row[8]
    
    @property
    def unit(self):
        return self.row[9]
    
    @property
    def electric_cost(self):
        return self.row[10]
    
    @property
    def water_cost(self):
        return self.row[11]
    
    @property
    def gas_cost(self):
        return self.row[12]
    
    @property
    def unlock_at_building_level(self):
        return self.row[13]
    
    def to_dict(self):
        values = {
            'cost_attempt': self.cost_attempt,
            'probability_per_attempt': self.probability_per_attempt,
            'raw_quality': self.raw_quality,
            'employees_needed': self.employees_needed,
            'quantity_per_attempt': self.quantity_per_attempt,
            'category_type': self.category_type,
            'building_type': self.building_type,
            'continents': self.continents,
            'unit': self.unit,
            'electric_cost': self.electric_cost,
            'water_cost': self.water_cost,
            'gas_cost': self.gas_cost,
            'unlock_at_building_level': self.unlock_at_building_level
        }

        return values


class ItemLoader(object):
    def __init__(self, path):
        self.path = path
    
    def load(self):
        """Load data"""
        try:
            with open(self.path) as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    item = ItemCSVRow(row)
                    obj, created = Item.objects.update_or_create(name=item.name, defaults=item.to_dict())
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
    category_type = models.CharField(max_length=255)  # str representation of category type
    building_type = models.TextField()  # str representation of list of building types
    continents = models.TextField()  # str representation of list of continents
    unit = models.CharField(max_length=255)
    electric_cost = models.DecimalField(max_digits=20, decimal_places=4)
    water_cost = models.DecimalField(max_digits=20, decimal_places=4)
    gas_cost = models.DecimalField(max_digits=20, decimal_places=4)
    unlock_at_building_level = models.IntegerField()

    objects = ItemManager()

    def building_type_to_dict(self) -> dict:
        """return the dictionary contains the building type that can produce the item"""
        return str(self.building_type).split(",")
    
    def continent_to_dict(self) -> dict:
        """retuurn the dictionary contains the continents """
        return str(self.continents).split(",")
    
    def belongs_to_continent(self, continent: str) -> bool:
        """Return true if this item belongs to this continent"""
        return continent.lower() in self.continent_to_dict()
    
    def belongs_to_building_type(self, building_type: str) -> bool:
        """return true if this item belongs to this building type"""
        return building_type.lower() in self.building_type_to_dict()