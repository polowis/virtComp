from app.models import Landscape, Building, Company
from app.models.constants import BuildingType
from app.models.core.product import Storage
from app.models.core.exception import UnableToConstructBuilding, NegativeLevel, CannotBuyBuildingOnRentLandscape
from typing import Union
from django.utils import timezone


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
    
    @classmethod
    def construct(cls, building_type: str, building_name: str, company: Company,
                  method_acquired: str, level: int, landscape: Landscape):
        """
        Call this function to create a building with the given type and name
        And the company instance that owns the building regardless of acquisition methods

        NOTE: The given landscape must owned by the given company

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
            builder: BuildingBuilder = cls(landscape, level, building_type, building_name)
            return builder.construct_building(company, method_acquired)

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
                building: Building = self.create_building()
                storage: Storage = self.create_storage(building)  # noqa
                return building
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
            'company_name': self.landscape.company.company_name,
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
    
    def create_storage(self, building: Building):
        """Create the storage associated with this building"""
        storage = Storage.objects.create_storage(building=building, max_capacity=building.max_storage)
        return storage