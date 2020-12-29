from __future__ import annotations
from django.db import models
import math
from typing import Union


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