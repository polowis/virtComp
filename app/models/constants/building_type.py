from __future__ import annotations
from django.db import models
from typing import Union
from app.models.core.exception import NegativeLevel


class BuildingTypeCSVRow(object):
    """The CSV class for handling BuildingType data
    
    DO NOT PASS HEADER
    """
    def __init__(self, row: list):
        if isinstance(row, list) and self._has_correct_format(row):
            self.row = row
        else:
            raise TypeError("row must be a list with length of 11")

    def _convert_bool_value(self, value: str) -> bool:
        """Convert to boolean object"""
        if value.lower() in ['true', '1', 'yes']:
            return True
        
        if value.lower() in ['false', '0', 'no']:
            return False

    @property
    def category(self) -> str:
        return self.row[0]

    @property
    def building_cost(self) -> float:
        return self.row[1]
    
    @property
    def building_rent(self) -> float:
        return self.row[2]
    
    @property
    def upgrade_cost(self) -> float:
        return self.row[3]
    
    @property
    def upgrade_cost_growth(self) -> Union[float, int]:
        return self.row[4]

    @property
    def max_employees(self) -> int:
        return self.row[5]
    
    @property
    def max_employees_growth(self) -> int:
        return self.row[6]
    
    @property
    def base_storage(self) -> int:
        return self.row[7]
    
    @property
    def base_storage_growth(self) -> Union[float, int]:
        return self.row[8]
    
    @property
    def can_sell(self) -> bool:
        return self._convert_bool_value(self.row[9])
    
    @property
    def can_produce(self) -> bool:
        return self._convert_bool_value(self.row[10])
    
    def _has_correct_format(self, row) -> bool:
        """This will return true if the given list of rows
        follow the required format.
        """
        return len(row) == 11



class BuildingTypeManager(models.Manager):
    def get_building_by_type(self, building_type: str) -> BuildingType:
        """Return BuildingType instance, raise error if not found"""

        if isinstance(building_type, str):
            return self.get(category=building_type)
        raise TypeError(f"Building type must be a string but got {type(building_type)}")
    
    def load_building_type(self, path_to_csv_file='csv_data/buildingType.csv', force_2d=False):
        pass


class BuildingType(models.Model):
    """The constant building type class of all types of buildings in game

    The class determines the statistics of buildings according to its type.

    To create or use the building, use class Building instead.

    All the buy costs here only applies when buying building from the
    government.

    NOTE: This class should not be used to edit or make any changes directly.
    Please consider using Building class instead. Building class is
    linked directly to this class.
    """
    name = models.CharField(max_length=255)

    # base level cost. This will be the buy cost base of this building
    # The formula determines the price of upgrading is as follows:
    # base_cost * cost_growth * building_level

    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)

    cost_growth = models.DecimalField(max_digits=5, decimal_places=3)

    # upgrade cost growth detemine how much it takes to upgrade the building
    upgrade_growth = models.DecimalField(max_digits=5, decimal_places=3)

    # base number of employees for this building. The formula to determine
    # numer of employees is as follow:
    # base_employee * employees_growth * building_level
    base_employees = models.IntegerField()
    employees_growth = models.DecimalField(max_digits=5, decimal_places=3)

    # base number of items can be stored for this building. The formula to
    # determine numer of item is as follow:
    # base_storage * storage_growth * building_level
    base_storage = models.IntegerField()
    storage_growth = models.DecimalField(max_digits=5, decimal_places=3)

    # determine if this type of building is being able to sell items to
    # customers
    can_sell = models.BooleanField()

    objects = BuildingTypeManager()


    def get_max_employees(self, level: int = 0) -> float:
        """Return the max employees for this type of building given the level
        if level is not provided. The base max employees will be returned instead

        if the level is a negative number, it will be considered as default value
        """
        if level <= 0:
            return self.base_employees
        else:
            if isinstance(level, int):
                return self.base_employees * self.employees_growth * level
            raise TypeError("Level must be an integer but got {}".format(type(level)))
    
    def get_max_storage(self, level: int = 0) -> float:
        """Return the max items can be stored in storage for this type of building given the level
        if level is not provided. The base max storage will be returned instead.

        if the level is a negative number, it will be considered as default value
        """
        if level <= 0:
            return self.base_storage
        else:
            if isinstance(level, int):
                return self.base_storage * self.storage_growth * level
            raise TypeError("Level must be an integer but got {}".format(type(level)))
    
    def get_buy_cost(self, level: int = 0) -> float:
        """
        This will return the amount of money to buy this type of building
        for level 0

        Companies are now allowed to create a building and buy it with over default level.
        It must start with level 0
        """
        return self.buy_cost
    
    def get_rent_cost(self, level: int = 0) -> float:
        """
        This will return the amount of money to buy this type of building
        for the given level

        :param level: The level of the building

        if the level is a negative number, it will be considered as default value
        """

        # if the given level negative, return the raw cost
        if level <= 0:
            return self.rent_cost
        else:
            if isinstance(level, int):
                return self.rent_cost * self.cost_growth * level
            raise NegativeLevel(level)
    
    def get_cost(self, method_acquired: str, level: int):
        """Return the matched cost rent or buy. This function assume that
        the method_acquired has already passed the validation process

        only the following methods are supported: ['buy', 'rent']

        raise NegativeLevel() if the given level is negative
        """
        return getattr(self, f'get_{method_acquired}_cost')(level)

