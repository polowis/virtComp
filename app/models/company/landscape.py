from django.db import models
from app.core.util.base import generate_unique_id
from app.models.company import Company
from django.utils import timezone
from typing import Union

class LandscapeManager(models.Manager):
    def get_all_landscape_by_company(self, lookup_company: Union[Company, str]):
        if type(lookup_company) is Company:
            return self.filter(company=lookup_company)
        if isinstance(company, str):
            return self.filter(company_name=lookup_company)
        raise TypeError("lookup_company must be a Company instance or a string of company name")

class Landscape(models.Model):
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.Integer()
    company_name = models.CharField(max_length=255, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    is_buy = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    last_collected_money_at = models.DateTimeField()

    objects = LandscapeManager()


    def buy(self, *args, **kwargs):
        """Buy the landscape. This function simple will try to update properties respectively.

        Alternatively, you can update it like the way how you normally do with django
        """
        if self.id:
            self.is_buy = True
            self.is_rent = False
            self.last_collected_money_at = timezone.now()
            return super(Landscape, self).save(*args, **kwargs)
        else:
            raise Exception("Unable to buy landscape")
    
    def rent(self, *args, **kwargs):
        """Rent a landscape. This function simple will try to update properties respectively.
        
        Alternatively, you can update it like the way how you normally do with django
        """
        if self.id:
            self.is_buy = False
            self.is_rent = True
            self.last_collected_money_at = timezone.now()
            return super(Landscape, self).save(*args, **kwargs)
        else:
            raise Exception("Unable to rent landscape")
    

    def on_rent(self) -> bool:
        """Return true if this landscape is on rent by a company"""
        return self.is_buy
    
    def already_bought(self) -> bool:
        """Return true if this landscape is already bought from a company"""
        return self.is_buy
    
    def can_be_purchased(self) -> bool:
        if self.company:
            return False
        return self.is_buy == False and self.is_rent == False
