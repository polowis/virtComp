from __future__ import annotations
from django.db import models
import random
import csv
from typing import Union
from app.core.services.loader import Loader
from setting import local_settings as env


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
    
    def to_dict(self):
        default_value: dict = {
            'cost': self.buy_cost,
            'rent': self.rent_cost,
            'max_land_cost': self.max_land_cost,
            'min_land_cost': self.min_land_cost
        }

        return default_value


class LandLoader(Loader):
    def __init__(self, path, use_direct_download=env.USE_DIRECT_SHEETS_DOWNLOAD):
        self.use_direct_download = use_direct_download
        if self.use_direct_download is True:
            super().__init__()
            self.sheet_name = 'land'
            self.spreadsheetsID = '1-3mrtO5tBDb1_Sn5YKZrp1avQ4chKD-x-U7c-gWpkuo'
            self.sheetID = '0'
            self.path = f'{self.file_saved_endpoint}/{self.sheet_name}.csv'

            self.pull_from_public_sheets()
        else:
            self.path = path
    
    def load(self):
        try:
            with open(self.path) as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    land: LandCSVRow = LandCSVRow(row)
                    obj, created = Land.objects.update_or_create(level=land.level,
                                                                 defaults=land.to_dict())
        except Exception as e:
            raise Exception(e)


class LandManager(models.Manager):
    def get_land_by_level(self, level: int) -> Land:
        return self.get(level=level)

    def get_supported_continents(self) -> list:
        return ['alantica', 'strovania', 'niaclausias', 'tastania', 'adionoris'
                'gonaucrit']

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
    
    def load_land(self, path_to_csv_file: Union[str, list[list]] = './csv_data/landData.csv', force_2d=False) -> None:
        """Load the land in given csv file.
        
        TODO: Allows to pass 2D array
        """
        if force_2d:
            self.load_land_from_2d_array(path_to_csv_file)
            return
        if isinstance(path_to_csv_file, str):
            loader = LandLoader(path_to_csv_file)
            loader.load()
    
    def default_continent(self):
        """Return the default land in case there is a missing continent"""
        return self.get_supported_continents()[0]  # return the first continent in the list

    def load_land_from_2d_array(self, objects):
        """
        Load the land from 2d array. It must not contains headers and
        has to follow the order

        level,buy_cost,rent_cost,max_land_cost,min_land_cost
        """
        for row in objects:
            land: LandCSVRow = LandCSVRow(row)
            default_value: dict = {
                'cost': land.buy_cost,
                'rent': land.rent_cost,
                'max_land_cost': land.max_land_cost,
                'min_land_cost': land.min_land_cost
            }
            obj, created = Land.objects.update_or_create(level=land.level,
                                                         defaults=default_value)


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
