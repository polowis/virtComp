from __future__ import annotations

from app.models.core import Company
from django.db import models
from app.core.util.base import generate_unique_id
from app.models.constants import Land
from django.utils import timezone
from typing import Union
import logging




logger = logging.getLogger(__name__)


class LandscapeManager(models.Manager):
    

    def get_landscape_by_company(self, company: Union[Company, str]) -> bool:
        if type(company) == Company:
            return self.filter(company=company)
        if isinstance(company, str):
            return self.filter(company_name=company)
        raise TypeError("lookup_company must be a Company instance or a string of company name")

    def get_rent_landscape_by_company(self,
                                      company: Union[Company, str]) -> bool:
        if type(company) == Company:
            return self.filter(company=company, is_rent=True)
        if isinstance(company, str):
            return self.filter(company_name=company, is_rent=True)

        raise TypeError("lookup_company must be a Company instance or a string of company name")
    
    def get_supported_continents(self):
        """Return the list of supported continents from Land class"""
        return Land.objects.get_supported_continents()

    def get_landscape_by_id(self, landscape_id: Union[int, str],
                            force_primary=False) -> Landscape:
        """Return the landscape instance by id.
        If force_primary is True, it will search for primary_key. Default is
        False

        Exception: Model not found exception will raise if there is no result
        found.

        """
        if force_primary:
            return self.get(id=landscape_id)
        return self.get(land_id=landscape_id)

    def landscape_is_available(self, landscape_id: str,
                               force_primary=False) -> bool:
        """Return true if landscape is available to purchase (buy/rent)

        If you wish to look up by primary_key, simple add force_primary=True,
        default is False
        """
        if force_primary:
            if isinstance(landscape_id, str):
                try:
                    landscape: Landscape = self.get(id=landscape_id)
                    return landscape.can_be_purchased
                except Exception as e:
                    logger.info(e)
                    raise TypeError("The landscape id cannot be found")
            raise TypeError("The landscape id must be a string")
        else:
            if isinstance(landscape_id, str):
                try:
                    landscape: Landscape = self.get(land_id=landscape_id)
                    return landscape.can_be_purchased
                except Exception as e:
                    logger.info(e)
                    raise TypeError("The landscape id cannot be found")
            raise TypeError("The landscape id must be a string")

    def create_land(self, continent: str) -> Landscape:
        """Create default land. To retreive supported continents

        You may use Land.objects.get_supported_continents() method

        :param continent: supported continent (str)

        return Landscape instance
        """
        if continent.lower() in Land.objects.get_supported_continents():
            level: int = Land.objects.get_random_land_level()
            land: Land = Land.objects.get_land_by_level(level)

            landscape: Landscape = self.create(level=level,
                                               buy_cost=land.get_land_cost(),
                                               rent_cost=land.get_rent_cost(),
                                               continent_cost=land.get_continent_buy_cost(),
                                               continent_rent=land.get_continent_rent_cost(),
                                               continent=continent.lower())
            landscape.save()
            return landscape
        else:
            raise Exception("Invalid continent name. Please see Land.objects.get_supported_continents()")

    def create_multiple_landscape(self, continent: str,
                                  number_of_land: int) -> None:
        """
        generate multiple landscape.
        This methods falls back to create_land method.

        This method will try to convert number_of_land into a number.
        Make sure that the continent provide is supported by virtComp

        :param continent: the contient you wish to create a landscape for
        :param number_of_land: the number of landscape to create

        return None
        """
        for i in range(int(number_of_land)):
            self.create_land(continent)

    def get_available_land(self):
        """Return list of Landscape objects that are not owned by any company"""
        return self.filter(company_name=None)


class Landscape(models.Model):
    """The base landscape models for create or upgrading anything related to land
    
    To only retrive default and base land details, consider using Land object instead.
    Alternatively, Landscape also supports retrieving information from Land object
    """
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.IntegerField()
    company_name = models.CharField(max_length=255, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    continent = models.CharField(max_length=255)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)

    # the cost of contient specific will be the extra cost.
    # buy cost + continent_cost
    continent_cost = models.DecimalField(max_digits=20, decimal_places=4)
    continent_rent = models.DecimalField(max_digits=20, decimal_places=4)

    is_buy = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    last_collected_money_at = models.DateTimeField(null=True)

    objects = LandscapeManager()

    def buy(self, *args, **kwargs):
        """Buy the landscape. This function simple will try to
        update properties respectively.

        Alternatively, you can update it like the way how you normally
        do with django
        """
        if self.id:
            self.is_buy = True
            self.is_rent = False
            self.last_collected_money_at = timezone.now()
            return self.save(*args, **kwargs)
        else:
            raise Exception("Unable to buy landscape")

    def rent(self, *args, **kwargs):
        """Rent a landscape. This function simple will try to update
        properties respectively.

        Alternatively, you can update it like the way how you normally
        do with django
        """
        if self.id:
            self.is_buy = False
            self.is_rent = True
            self.last_collected_money_at = timezone.now()
            return self.save(*args, **kwargs)
        else:
            raise Exception("Unable to rent landscape")

    def on_rent(self) -> bool:
        """Return true if this landscape is on rent by a company"""
        return self.is_rent

    def already_bought(self) -> bool:
        """Return true if this landscape is already bought from a company"""
        return self.is_buy

    def can_be_purchased(self) -> bool:
        """Return true if this landscape can be purchased"""
        if self.company:
            return False
        return not self.is_buy and not self.is_rent
    
    def company_able_to_purchase(self, company: Company) -> bool:
        """Return true if this given company instance be able to buy the land
        
        This function will check for balance left in company
        """
        if type(company) == Company:
            return company.balance >= self.buy_cost

    def save(self, *args, **kwargs):
        """Save the object to the database"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def purchase_landscape(self, company: Company) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape
        """
        if isinstance(company, Company):
            self.company = company
            self.company_name = company.company_name
            company_new_balance = company.balance - self.buy_cost
            company.balance = company_new_balance
            company.save()
            self.buy()
        else:
            raise TypeError("The company param must be an instance of Company but got {} instead".format(type(company)))
    
    def required_extra_continent_cost(self, company: Company):
        """
        Return true if the there is an extra cost for owning a land
        outside company registered country

        Return False if there is no extra cost or invalid company object passing
        """
        if type(company) == Company:
            return company.continent != self.continent
        return False
    
    def get_extra_contient_cost(self, company: Company, method_acquired: str) -> Union[models.DecimalField, int]:
        """This method return the extra cost for owning the land that outside of
        company registered continent.

        :param company: the company instance that wants to buy the land

        :param method_acquired: the method of owning the land that the company wish to own
        must be present in string format

        return extra cost in number format
        """
        if self.required_extra_continent_cost(company):
            return getattr(self, method_acquired)
        return 0