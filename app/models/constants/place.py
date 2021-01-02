from __future__ import annotations
from django.db import models
import math
import random
from typing import Union, Dict
import csv


class PlaceRow(object):
    """The constant place row must be correctly format as follow
    
    x,y,name,group,continent

    where x and y denote the coordinates of the place (present in number format either int or float)
    """
    def __init__(self, row: list):
        if self._has_correct_format(row):
            self.row = row
        else:
            raise TypeError("The imported row is incorrectly formatted")
    
    @property
    def x(self) -> Union[int, float]:
        return self.row[0]
    
    @property
    def y(self) -> Union[int, float]:
        return self.row[1]
    
    @property
    def name(self) -> str:
        return self.row[2]
    
    @property
    def group(self) -> str:
        return self.row[3]
    
    @property
    def continent(self) -> str:
        return self.row[4]
    
    def _has_correct_format(self, row) -> bool:
        """This will return true if the given list of rows
        follow the required format.
        """
        return len(row) == 5
    
    def as_dict(self) -> Dict[str, str]:
        """Return a dictionary of corresponding fields"""
        default_value: dict = {
            'x': self.x,
            'y': self.y,
            'group': self.group,
            'continent': self.continent,
        }

        return default_value


class PlaceManager(models.Manager):
    def create_place(self, x: int, y: int, name: str, group: str, continent: str):
        place = self.create(x, y, name, group, continent)
        return place
    
    def distance_from(self, place1: Place, place2: Place, force_round=False) -> Union[int, float]:
        """
        Calculate the distance from place1 to place2 using euclidean distance function.
        Only support for 2 dimesions

        If force_round is True, the result will be rounded down to nearest integer. Currently
        not support for rounding up.

        :param place1: Place instance

        :param place2: Place instance
        """
        # euclidean distance between two places
        scale_factor = 50  # the scale factor to match real distance
        distance = math.sqrt((place1.x - place2.x)**2 + (place1.y - place2.y)**2)
        return math.floor(distance * scale_factor) if force_round else distance * scale_factor
    
    def load_data(self, data: Union[str, list[list]] = "./csv_data/place.csv"):
        """Load the place data from a CSV file or as a 2d array. Both are accepted.
        If the places names are already presented, it will update the data respectively
        """
        if isinstance(data, str):  # assume that if the given data is in string format, then it must be the path
            try:
                with open(data) as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        place: PlaceRow = PlaceRow(row)
                        default_value = place.as_dict()
                        obj, created = self.update_or_create(name=place.name, defaults=default_value)
            except Exception as e:
                raise Exception(e)
    
    def get_supported_place(self) -> list[dict]:
        """Get supported place name
        
        Return a list containing the dictionary as formatted below:

        [{'name': 'place_name'}]
        """
        return self.all().values('name')

    def get_random_place(self, continent: str) -> str:
        """Return the random place name as string from a given continent"""
        places = list(self.filter(continent=continent).values('name'))
        chosen_place = places[math.floor(random.random() * len(places))]
        return chosen_place['name']
    
    def belongs_to(self, place_name: str, continent: str):
        """Check if the given place belongs to the correct given continent"""
        try:
            place: Place = self.get(name=place_name)
            return place.continent == continent
        except Place.DoesNotExist:
            return False


class Place(models.Model):
    """The constant place model to deal with place"""
    x = models.IntegerField()
    y = models.IntegerField()
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    continent = models.CharField(max_length=255)

    objects = PlaceManager()

    def distance_to(self, place: Place, force_round=False):
        """
        If force_round is True, the result will be rounded down to nearest integer. Currently
        not support for rounding up.

        :param place1: Place instance
        """
        scale_factor = 50  # the scale factor to match real distance
        distance = math.sqrt((self.x - place.x)**2 + (self.y - place.y)**2)
        return math.floor(distance * scale_factor) if force_round else distance * scale_factor