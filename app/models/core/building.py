from __future__ import annotations
from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core import Company
from .landscape import Landscape
from app.models.constants import BuildingType
import random
from app.models.core.exception import UnableToConstructBuilding
from typing import Union
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from app.models.constants import Item


class BuildingManager(models.Manager):
    """The manager for building object"""

    def create_building(self, building_type: str, building_name: str, company: Company,
                        method_acquired: str, level: int, landscape: Landscape) -> Building:
        """
        DEPRECATED: DO NOT USE THIS METHOD. USE BuildingBuilder class instead

        Call this function to create a building with the given type and name
        And the company instance that owns the building regardless of acquisition methods

        NOTE: The given landscape must own by the given company

        There are two things to consider when owning building, create a building and owning it.
        This function should only be used to own a building that has never been created

        throw exception: CannotBuyBuildingOnRentLandscape, UnableToConstructBuilding

        return Building instance

        """

        raise NotImplementedError("Please use BuildingBuilder class instead")
    
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
    
    def can_produce(self, item: Item) -> bool:
        """return true if this type of building can produce the item
        this will check for building location and type

        The item provided must be the item instance but not the string
        """
        return (item.belongs_to_continent(str(self.landscape.continent))
                and item.belongs_to_building_type(str(self.building_type)))  # noqa  