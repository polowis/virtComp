from __future__ import annotations
from django.db import models
import random
import csv


class LandCSVRow(object):
    """The base row for readability purpose
    
    Assuming that the csv file has the exact same format

    level,buy_cost,rent_cost,max_land_cost,min_land_cost
    """
    def __init__(self, row: list):
        if isinstance(row, list) and self._has_correct_format(row):
            self.row = row
        else:
            raise TypeError("row must be a list with length of 5")
    
    @property
    def level(self) -> int:
        return self.row[0]

    @property
    def rent_cost(self) -> float:
        return self.row[2]
    
    @property
    def buy_cost(self) -> float:
        return self.row[1]

    @property
    def max_land_cost(self) -> float:
        return self.row[3]

    @property
    def min_land_cost(self) -> float:
        return self.row[4]
    
    def _has_correct_format(self, row) -> bool:
        """This will return true if the given list of rows
        follow the required format.
        """
        return len(row) == 5


class LandManager(models.Manager):
    def get_land_by_level(self, level: int) -> Land:
        return self.get(level=level)

    def get_supported_continents(self) -> list:
        return ['asia', 'south america', 'north america', 'europe',
                'oceania', 'africa']

    def get_probability(self) -> list:
        """
        return the list of probability of getting land on a certain
        level respectively
        """
        return [0.23, 0.15, 0.13, 0.1, 0.09, 0.08, 0.06, 0.06, 0.05,
                0.03, 0.02]

    def get_supported_land_level(self) -> list:
        """return a list of supported Land level"""
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def get_random_land_level(self) -> int:
        """Return a random land level"""
        return random.choices(self.get_supported_land_level(),
                              self.get_probability(), k=1)[0]

    def get_random_continent(self) -> str:
        """get a random continent"""
        continent_list: list = self.get_supported_continents()
        return random.choice(continent_list)
    
    def load_land(self, path_to_csv_file: str = './csv_data/landData.csv') -> None:
        """Load the land in given csv file.
        
        TODO: Allows to pass dictionary of lists
        """
        if isinstance(path_to_csv_file, str):
            try:
                with open(path_to_csv_file) as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        land: LandCSVRow = LandCSVRow(row)
                        default_value: dict = {
                            'cost': land.buy_cost,
                            'rent': land.rent_cost,
                            'max_land_cost': land.max_land_cost,
                            'min_land_cost': land.min_land_cost
                        }
                        obj, created = Land.objects.update_or_create(level=land.level,
                                                                     defaults=default_value)
            except FileNotFoundError:
                raise FileNotFoundError("The file for csv file was not found")



class Land(models.Model):
    level = models.IntegerField()
    cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent = models.DecimalField(max_digits=20, decimal_places=4)
    max_land_cost = models.DecimalField(max_digits=20, decimal_places=4)
    min_land_cost = models.DecimalField(max_digits=20, decimal_places=4)

    objects = LandManager()

    def __str__(self):
        return self.level

    def get_land_cost(self):
        """generate land cost. This will return a random result in the range
        of 10% of land base cost
        """
        return random.uniform(float(self.min_land_cost),
                              float(self.max_land_cost))

    def get_rent_cost(self):
        """generate rent cost.
        This simply return the rent cost property
        """
        return self.rent

    def generate_continent_cost(self, base_cost):
        return random.uniform(float(base_cost) * 0.08,
                              float(base_cost) * 0.12)

    def get_continent_buy_cost(self):
        """Return the continent buy cost"""
        return self.generate_continent_cost(self.cost)

    def get_continent_rent_cost(self):
        """return the continent rent cost"""
        return self.generate_continent_cost(self.rent)
