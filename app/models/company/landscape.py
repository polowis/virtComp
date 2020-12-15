from django.db import models
from app.core.util.base import generate_unique_id
from app.models.company import Company
from django.utils import timezone
from typing import Union
from app.models import Landscape
import logging

logger = logging.getLogger(__name__)


class LandscapeManager(models.Manager):
    def get_landscape_by_company(self, company: Union[Company, str]) -> bool:
        if type(company) is Company:
            return self.filter(company=company)
        if isinstance(company, str):
            return self.filter(company_name=company)
        raise TypeError("lookup_company must be a Company instance or a " +
                        "string of company name")

    def get_rent_landscape_by_company(self,
                                      company: Union[Company, str]) -> bool:
        if type(company) is Company:
            return self.filter(company=company, is_rent=True)
        if isinstance(company, str):
            return self.filter(company_name=company, is_rent=True)

        raise TypeError("lookup_company must be a Company instance or" +
                        " a string of company name")

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

    def create_land(self, level: int, buy_cost: int,
                    rent_cost: int) -> Landscape:
        """Create default land

        :param level: the level of the landscape

        :param buy_cost: the cost to buy the landscape

        :param rent_cost: the cost to rent the landscape

        return Landscape instance
        """
        landscape: Landscape = self.create(level=level, buy_cost=buy_cost,
                                           rent_cost=rent_cost)
        return landscape


class Landscape(models.Model):
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.Integer()
    company_name = models.CharField(max_length=255, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    continent = models.CharField(max_length=255)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)
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
        return self.is_buy

    def already_bought(self) -> bool:
        """Return true if this landscape is already bought from a company"""
        return self.is_buy

    def can_be_purchased(self) -> bool:
        """Return true if this landscape can be purchased"""
        if self.company:
            return False
        return not self.is_buy and not self.is_rent

    def save(self, *args, **kwargs):
        """Save the object to the database"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
