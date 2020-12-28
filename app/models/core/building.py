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
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


class BuildingBuilder(object):
    """
    This is just for constructing the building. For buying the building.
    Please see alternative method

    It will include the cost of constructing the building.

    Usage: call construct_building()

    Constructor: Landscape instance. The land to constructing the building on top
    """
    def __init__(self, landscape: Landscape, level: int, building_type: str, building_name: str):
        """
        Constructor: Landscape instance. The land to constructing the building on top
        """
        self.landscape = landscape
        self.level = level
        self.building_type = building_type
        self.building_name = building_name
        self.buildingType_instance = None
        self.method_acquired = None

    def can_build(self, company: Company, method_acquired: str) -> bool:
        """
        Return true if can build the building on this landscape
        
        This method only check for whether or not the
        company able to construct the building with given lEVEL and company owner
        assocciated with landscape.

        This method does not check for anything else
        """
        self.method_acquired = method_acquired
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
                return self.create_building()
            except ValueError:
                raise UnableToConstructBuilding()
        else:
            raise UnableToConstructBuilding()
    
    def process_transaction(self, method_acquired: str):
        """
        Proccessing transaction upon owning this building. Do not call this method directly.
        
        Accept one parameter: method_acquired

        raise ValueError
        """
        building_type: BuildingType = self.get_building_details()
        if building_type is not None:
            self.buildingType_instance = building_type
            try:
                cost = building_type.get_cost(method_acquired.lower(), self.level)
                self.cost = cost
                company = self.landscape.company
                company.balance -= cost
                if company.balance < 0:
                    raise ValueError("Company balance must be positive")
                company.save()
            except NegativeLevel:
                raise ValueError("The level must be negative")

    def get_building_details_as_dict(self) -> dict:
        """
        Return the dictionary of buildingtyp details
        If you're looking for an instance, refer to get_building_details() instead
        """
        details: dict = {
            'building_type': self.building_type,
            'building_name': self.building_name,
            'landscape': self.landscape,
            'company': self.landscape.company,
            'current_level': self.level,
            'max_storage': self.buildingType_instance.get_max_storage(self.level),
            'max_employees': self.buildingType_instance.get_max_employees(self.level),
            'is_rent': self.method_acquired == 'rent',
            'is_buy': self.method_acquired == 'buy',
            #  the price that when first bought this building regardless of method of acquiring
            'buy_cost': self.cost,
            'rent_cost': self.cost if self.method_acquired == 'rent' else None,
            'last_collected_money_at': timezone.now()
        }
        return details

    def create_building(self) -> Building:
        """Create the building and save to the database.
        Do not call this method directly.
        """
        details = self.get_building_details_as_dict()
        building: Building = Building.objects.create(**details)
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
                
            # construct the building
            builder: BuildingBuilder = BuildingBuilder(landscape, level, building_type, building_name)
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
    """
    The Building model for handling anything related to building (a building of a company)

    DO NOT USE BuildingType class. But this class instead
    """
    building_id = models.CharField(max_length=255, default=generate_unique_id)
    building_type = models.CharField(max_length=255)
    building_name = models.CharField(max_length=255)

    # the current level of this type of building
    current_level = models.IntegerField()

    company_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # the storage field for this building
    current_storage = models.IntegerField(default=0)
    max_storage = models.IntegerField()

    current_employees = models.IntegerField(default=0)
    max_employees = models.IntegerField()

    is_buy = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4, null=True)

    landscape = models.OneToOneField(Landscape, on_delete=models.CASCADE, primary_key=True)


    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    last_collected_money_at = models.DateTimeField()

    objects = BuildingManager()

    @property
    def model(self) -> BuildingType:
        """
        Return BuildingType instance
        """
        return BuildingType.objects.get_building_by_type(self.building_type)
    
    def save(self, *args, **kwargs) -> None:
        try:
            self.landscape
            if not self.created_at:
                self.created_at = timezone.now()
            self.updated_at = timezone.now()
            return super().save(*args, **kwargs)
        except ObjectDoesNotExist:
            raise UnableToConstructBuilding("Cannot construct building on unknown landscape")
    
    def belongs_to(self, landscape: Landscape):
        """Return true if this building belongs to the given landscape instance"""
        if isinstance(landscape, Landscape):
            try:
                building_landscape = self.landscape
                return landscape == building_landscape
            except ObjectDoesNotExist:
                return False
        return False
    
    def owned_by(self, company: Union[Company, str]):
        """Return true if this building owned by given company
        
        This method check if landscape attribute exists then
        called the owned_by method from landscape instance

        Return False if not found and not match
        """
        try:
            building_landscape: Landscape = self.landscape
            return building_landscape.owned_by(company)
        except ObjectDoesNotExist:
            return False
    
    def needs_to_pay_rent(self):
        """Return true if the company needs to pay rent for this building"""
        if self.is_rent:
            now: datetime = timezone.now()
            return now - timedelta(days=7) >= self.last_collected_money_at
        return False
    
    def pay_rent(self, company: Company) -> None:
        """Pay the required rent. This method calls needs_to_pay_rent method directly
        to check if the building needs to be paid. This is to ensure that user do not pay
        too soon or too late.
        """
        if self.needs_to_pay_rent():
            # Only the same owner can pay the rent
            if self.company == company:
                company.balance -= self.rent_cost
                if company.balance < 0:
                    raise ValueError("Insufficient amount of money to pay")
                company.save()
                self.last_collected_money_at = timezone.now()
    
    def rent_overdue(self):
        """
        Return true if the rent is overdue. This will be usually one month (30) days
        """
        if self.is_rent:
            now: datetime = timezone.now()
            return now - timedelta(days=30) >= self.last_collected_money_at
        return False