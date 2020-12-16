from __future__ import annotations
from django.db import models
import random


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
        return random.choices(self.get_probability(),
                              self.get_supported_land_level(), k=1)[0]

    def get_random_continent(self) -> str:
        """get a random continent"""
        continent_list: list = self.get_supported_continents()
        return random.choice(continent_list)


class Land(models.Model):
    level = models.IntegerField()
    cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent = models.DecimalField(max_digits=20, decimal_places=4)
    max_land_cost = models.DecimalField(max_digits=20, decimal_places=4)
    min_land_cost = models.DecimalField(max_digits=20, decimal_places=4)

    objects = LandManager()

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
