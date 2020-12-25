from __future__ import annotations
from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core import Company
from app.models.core import Landscape
from app.models.constants import BuildingType
import random
from app.models.core.exception import CannotBuyBuildingOnRentLandscape
from app.models.core.exception import NegativeLevel, UnableToConstructBuilding
from typing import Union


class BuildingBuilder(object):
    """
    This is just for constructing the building. For buying the building.
    Please see alternative method

    It will include the cost of constructing the building

    Constructor: Landscape instance. The land to constructing the building on top
    """
    def __init__(self, landscape: Landscape, level: int, building_type: str):
        """
        Constructor: Landscape instance. The land to constructing the building on top
        """
        self.landscape = landscape
        self.level = level
        self.building_type = building_type

    def can_build(self, company: Company, method_acquired: str) -> bool:
        """
        Return true if can build the building on this landscape
        
        This method only check for whether or not the
        company able to construct the building with given lEVEL and company owner
        assocciated with landscape.

        This method does not check for anything else
        """
        if self.landscape.owned_by(company):
            if method_acquired == 'rent':
                return self.landscape.can_create_rent_building(self.level)
            if method_acquired == 'buy':
                return self.landscape.can_create_building(self.level)
        return False
    
    def get_building_details(self) -> Union[BuildingType, None]:
        """
        Return the buildingtype instance of None if none is found
        """
        try:
            return BuildingType.objects.get_building_by_type(self.building_type)
        except BuildingType.DoesNotExist:
            return None
    
    def construct_building(self, company: Company, method_acquired: str):
        """
        Construct the building. Only use this method to construct the building
        regardless of method of acquisition
        """
        if self.can_build(company, method_acquired):
            try:
                self.process_transaction(method_acquired)
                self.create_building()
            except ValueError:
                raise UnableToConstructBuilding()
    
    def process_transaction(self, method_acquired: str):
        """
        Proccessing transaction upon owning this building. Do not call this method directly.
        
        Accept one parameter: method_acquired

        raise ValueError
        """
        building_type: BuildingType = self.get_building_details()
        if building_type is not None:
            try:
                cost = building_type.get_cost(method_acquired.lower(), self.level)
                company = self.landscape.company
                company.balance -= cost
                if company.balance < 0:
                    raise ValueError("Company balance must be positive")
                company.save()
            except NegativeLevel:
                raise ValueError("The level must be negative")

    def create_building(self) -> Building:
        """Create the building and save to the database.
        Do not call this method directly.
        """
        building: Building = Building.objects.create(building_type=self.building_type,
                                                     building_name=self.building_name,
                                                     company=self.landscape.company,
                                                     level=self.level)
        return building


class BuildingManager(models.Manager):
    """The manager for building object"""

    def create_building(self, building_type: str, building_name: str, company: Company,
                        method_acquired: str, level: int, landscape: Landscape) -> Building:
        """Call this function to create a building with the given type and name
        And the company instance that owns the building regardless of acquisition methods

        NOTE: The given landscape must own by the given company

        There are two things to consider when owning building, create a building and owning it.
        This function should only be used to own a building that has never been created

        throw exception: CannotBuyBuildingOnRentLandscape, UnableToConstructBuilding

        return Building instance
        """

        supported_methods_acquired = ['buy', 'rent']

        method_acquired = method_acquired.lower()

        if method_acquired in supported_methods_acquired:

            # if the given landscape is on rent and method of acquiring is buy
            if landscape.on_rent() and method_acquired == 'buy':
                raise CannotBuyBuildingOnRentLandscape()
            builder: BuildingBuilder = BuildingBuilder(landscape, level, building_type)
            return builder.construct_building(company, method_acquired)
    
    def get_building_buy_cost(self, building: BuildingType, level: int):
        """This method returns the cost of buying this type of building given the level"""
        return building.get_buy_cost(level)
    
    def get_building_storage(self, building: BuildingType, level: int):
        """This method returns the maximum items can be stored this type of building given the level"""
        return building.get_max_storage(level)
    
    def generate_building_level(self, landscape: Landscape, level: int, random_level: bool = False):
        """Generate building level.

        This method will try to check if the landscape level is lower than the given level. The building level
        can never be greater than landscape level
        
        :param landscape: Landscape The landscape instance

        :param level: int The building level you wish to generate

        :param random_level: bool if it's true, the function will try to generate the random level
        in given range. default to False
        """
        if landscape.level < level:
            raise Exception("You cannot create a building level higher than land level")
        
        if random_level:
            return random.choice([i for i in range(0, level + 1)])
        else:
            return level
    

class Building(models.Model):
    building_id = models.CharField(max_length=255, default=generate_unique_id)
    building_type = models.CharField(max_length=255)
    building_name = models.CharField(max_length=255)

    # the current level of this type of building
    current_level = models.IntegerField()

    company_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # the storage field for this building
    current_storage = models.IntegerField()
    max_storage = models.IntegerField()

    current_employee = models.IntegerField(default=0)
    max_employee = models.IntegerField()

    is_buy = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)

    landscape = models.OneToOneField(Landscape, on_delete=models.CASCADE,
                                     primary_key=True)
    last_collected_money_at = models.DateTimeField()

    objects = BuildingManager()

    @property
    def model(self) -> BuildingType:
        """
        Return BuildingType instance
        """
        return BuildingType.objects.get_building_by_type(self.building_type)