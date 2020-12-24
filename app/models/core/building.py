from __future__ import annotations
from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core import Company
from app.models.core import Landscape
from app.models.constants import BuildingType
import random


class BuildingManager(models.Manager):
    def create_building(self, building_type: str, building_name: str, company: Company,
                        method_acquired: str, level: int) -> Building:
        """Call this function to create a building with the given type and name
        And the company instance that owns the building regardless of acquisition methods

        There are two things to consider when owning building, create a building and owning it.
        This function should only be used to own a building that has never been created

        return Building instance
        """
        supported_methods_acquired = ['buy', 'rent']

        building_details: BuildingType = BuildingType.objects.get_building_by_type(building_type)

        if method_acquired.lower() in supported_methods_acquired:
            self._construct_building(building_details, level, company, method_acquired.lower())
            building: Building = self.create(building_type=building_type,
                                             building_name=building_name,
                                             company=company)

            return building
    
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
    
    def _construct_building(self, building: BuildingType, level: int, company: Company,
                            method_acquired: str):
        """
        Do not call this method directly

        Use create_building() instead.
        
        """
        cost = building.get_cost(method_acquired.lower())
        company.balance -= cost
        if company.balance < 0:
            raise ValueError("Company balance must be positive")
        company.save()
        
    

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