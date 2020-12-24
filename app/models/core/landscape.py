from __future__ import annotations

from app.models.core import Company
from django.db import models
from app.core.util.base import generate_unique_id
from app.models.constants import Land
from django.utils import timezone
from typing import Union
import logging
from setting import local_settings as env
import random
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class LandscapeManager(models.Manager):
    """
    The landscape manager.
    """

    def get_single_landscape_by_company(self, landscape_id: Union[str, int], company: Company,
                                        force_primary: bool = False) -> Landscape:
        """
        This method return the landscape instance with given id and company.
        The given company must own this landscape

        if force_primary is True then it will look up for index key of the landscape in the database
        default is False. You will need to make sure that param landscape_id is the actual index key
        of the landscape not the land_id

        :param company: the company instance or the company name. Both are fine but required
        """
        if force_primary:
            if type(company) == Company:
                return self.get(id=landscape_id, company=company)
            if isinstance(company, str):
                return self.get(id=landscape_id, company=company.company_name)
            raise TypeError("The company must be a string or a company instance but got: %s" % type(company))
        else:
            if type(company) == Company:
                return self.get(land_id=landscape_id, company=company)
            if isinstance(company, str):
                return self.get(land_id=landscape_id, company=company.company_name)
            raise TypeError("The company must be a string or a company instance but got: %s" % type(company))

    def get_landscape_by_company(self, company: Union[Company, str], force_json: bool = False, values_list=None):
        """Return the list of landscape instance that are owned by the given company

        Set force_json to True to return list of objects
        """
        if type(company) == Company:
            if force_json:
                return list(self.filter(company=company).values())
            return self.filter(company=company)
        if isinstance(company, str):
            if force_json:
                return list(self.filter(company=company).values())
            return self.filter(company_name=company)
        raise TypeError("lookup_company must be a Company instance or a string of company name")

    def get_rent_landscape_by_company(self, company: Union[Company, str]) -> bool:
        """Return the list of landscape instance that on rent by the given company
        The param company can be either a string representing company name or a company instance
        """
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

    def landscape_is_available(self, landscape_id: Union[str, int],
                               force_primary: bool = False) -> bool:
        """Return true if landscape is available to purchase (buy/rent)

        If you wish to look up by primary_key, simple add force_primary=True,
        default is False
        """
        if force_primary:
            if isinstance(landscape_id, str) or isinstance(landscape_id, int):
                try:
                    landscape: Landscape = self.get(id=landscape_id)
                    return landscape.can_be_purchased()
                except Exception as e:
                    logger.info(e)
                    raise TypeError("The landscape id cannot be found")
            raise TypeError("The landscape id must be a string")
        else:
            if isinstance(landscape_id, str) or isinstance(landscape_id, int):
                try:
                    landscape: Landscape = self.get(land_id=landscape_id)
                    return landscape.can_be_purchased()
                except Exception as e:
                    logger.info(e)
                    raise TypeError("The landscape id cannot be found")
            raise TypeError("The landscape id must be a string")
    
    def _generate_default_landscape(self, continent: str):
        """Return the landscape instance but DOES NOT SAVE INTO DATABASE
        
        consider using create_land() instead
        """
        level: int = Land.objects.get_random_land_level()
        land: Land = Land.objects.get_land_by_level(level)

        return Landscape(level=level, buy_cost=land.get_land_cost(), rent_cost=land.get_rent_cost(),
                         continent_cost=land.get_continent_buy_cost(),
                         continent_rent=land.get_continent_rent_cost(),
                         continent=continent.lower())

    def create_land(self, continent: str) -> Landscape:
        """Create default land. To retreive supported continents

        You may use Land.objects.get_supported_continents() method

        :param continent: supported continent (str)

        return Landscape instance
        """
        if continent.lower() in Land.objects.get_supported_continents():
            landscape: Landscape = self._generate_default_landscape(continent)
            landscape.save(force_insert=True)
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
        lands = [self._generate_default_landscape(continent) for i in range(int(number_of_land))]
        self.bulk_create(lands)

    def get_available_land(self):
        """Return list of Landscape objects that are not owned by any company"""
        return self.filter(company_name=None)
    
    def get_random_available_land(self, json_format=True):
        """get random land available to be purchased"""
        if json_format:
            landscapes_available = self.get_available_land()
            random_lands = random.sample(list(landscapes_available.values()), env.MAXIMUM_lAND_VIEW)
            return random_lands
        else:
            raise Exception("Not available in normal format.")


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

    is_selling = models.BooleanField(default=True)

    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    # will be used to detect rent time
    last_collected_money_at = models.DateTimeField(null=True)

    objects = LandscapeManager()

    def buy(self, *args, **kwargs):
        """Buy the landscape. This function simple will try to
        update properties respectively.

        NOTE: This does not subtract the required cost to obtain the landscape
        but rather updating properties and save them to the database

        Alternatively, you can update it like the way how you normally
        do with django

        This should not be called directly. Consider calling purchase_landscape for buying

        """
        if self.id:
            self.is_buy = True
            self.is_rent = False
            self.is_selling = False
            self.last_collected_money_at = timezone.now()
            return self.save(*args, **kwargs)
        else:
            raise Exception("Unable to buy landscape")

    def rent(self, *args, **kwargs):
        """Rent a landscape. This function simple will try to update
        properties respectively.

        NOTE: This does not subtract the required cost to obtain the landscape
        but rather updating properties and save them to the database

        Alternatively, you can update it like the way how you normally
        do with django

        This should not be called directly. Consider calling rent_landscape for renting
        """
        if self.id:
            self.is_buy = False
            self.is_rent = True
            self.is_selling = False
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
        return self.is_selling
    
    def company_able_to_purchase(self, company: Company, method_acquired: str) -> bool:
        """Return true if this given company instance be able to buy the land
        
        This function will check for balance left in company
        """
        supported_methods_acquired = ['buy', 'rent', 'buy_cost', 'rent_cost']
        if method_acquired.lower() in supported_methods_acquired and isinstance(method_acquired, str):
            if not method_acquired.lower().endswith('_cost'):
                method_acquired = method_acquired.lower() + '_cost'
            
            if type(company) == Company:
                return company.balance >= getattr(self, method_acquired)
        raise TypeError("method_acquired param must be in supported methods but got %s instead" % method_acquired)

    def save(self, *args, **kwargs) -> None:
        """Save the object to the database"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def purchase_landscape(self, company: Company) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        This function does not call company_able_to_purchase_method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(company, Company):
            self.company = company
            self.company_name = company.company_name
            company_new_balance = company.balance - self.buy_cost
            if company_new_balance < 0:
                raise ValueError("Company balance must be positive")
            company.balance = company_new_balance
            company.save()
            self.buy()
        else:
            raise TypeError("The company param must be an instance of Company but got {} instead".format(type(company)))

    def rent_landscape(self, company: Company) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        This function does not call company_able_to_purchase_method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(company, Company):
            self.company = company
            self.company_name = company.company_name
            company_new_balance = company.balance - self.rent_cost
            if company_new_balance < 0:
                raise ValueError("Company balance must be positive")
            company.balance = company_new_balance
            company.save()
            self.rent()
        else:
            raise TypeError("The company param must be an instance of Company but got {} instead".format(type(company)))

    def required_extra_continent_cost(self, company: Company) -> bool:
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
        must be present in string format (case insensitive but underscore must present).
        Supported format: (continent_cost, continent_rent)

        return extra cost in number format. If the company does not required extra continent cost
        this method will return 0
        """

        # preventing access to other attributes
        supported_methods_acquired = ['continent_cost', 'continent_rent']

        if self.required_extra_continent_cost(company) and method_acquired.lower() in supported_methods_acquired:
            return getattr(self, method_acquired.lower())
        return 0
    
    def put_on_sale(self, company: Company, price: float) -> None:
        """
        Put this landscape on sale. Currently only support buy method
        This also means that the given company must own this landscape
        """
        if type(company) == Company and isinstance(price, float):
            if self.company_name == company.company_name and self.already_bought():
                # only is the given company owns this landscape
                self.is_selling = True
                self.buy_cost = price
                self.save()
    
    def owned_by(self, company: Union[Company, str]) -> bool:
        """Return True if this landscape is owned by given company"""
        if isinstance(company, str):
            return self.company_name == company
        elif type(company) == Company:
            return self.company == company
        raise TypeError("Company must be a string or a Company instance")
    
    def needs_to_pay_rent(self):
        """Return true if the company needs to pay rent"""
        if self.is_rent:
            now: datetime = timezone.now()
            return now - timedelta(days=7) >= self.last_collected_money_at
        return False
    
    def pay_rent(self, company: Company) -> None:
        """Pay the required rent. This method calls needs_to_pay_rent method directly
        to check if the landscape needs to be paid. This is to ensure that user do not pay
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
