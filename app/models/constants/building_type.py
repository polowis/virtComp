from __future__ import annotations
from django.db import models


class BuildingTypeManager(models.Manager):
    def get_building_by_type(self, building_type: str) -> BuildingType:
        """Return BuildingType instance, raise error if not found"""

        if isinstance(building_type, str):
            return self.get(category=building_type)
        raise TypeError(f"Building type must be a string but got {type(building_type)}")


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
