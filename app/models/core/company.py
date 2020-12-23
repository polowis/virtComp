from __future__ import annotations
import app.models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.core.util.base import generate_unique_id
from app.core.validator.base import Validator
import logging
logger = logging.getLogger(__name__)



class CompanyManager(models.Manager):
    def create_company(self, company_name: str, owner_object: User, continent: str = 'asia') -> Company:
        """Create a company and save them to database. Return Company object

        :param company_name: Name of the company

        :param owner_object: The user object

        :continent: the continent of the company

        throw exception if unable to create
        """
        if self.can_create_company(company_name):
            company = self.create(company_name=company_name, owner_name=owner_object.username,
                                  owner=owner_object, continent=continent)
            return company
        raise Exception("Unable to create company. The company might be already exists")

    def has_valid_company_name(self, company_name: str) -> bool:
        """Return true if the given company name is valid to be registered
        
        The ideal name is alphanumeric (no whitespace allows, although, this will be taken into consideration)
        and lower than 15 characters
        """
        return Validator.is_alphanumeric(company_name) and Validator.has_below(company_name, 20)

    def company_exists(self, company_name: str) -> bool:
        """Return true if the company with the given name already exists"""
        try:
            self.get(company_name=company_name)
            return True
        except Company.DoesNotExist:
            return False
    
    def can_create_company(self, company_name: str) -> bool:
        """Return true if the given company can be created
        
        This will ensure that the company name has not been registered and has a valid name
        """
        return not self.company_is_exists(company_name) and self.has_valid_company_name(company_name)


class Company(models.Model):
    """
    The company model. Use this class if you want to create a company associated with given user
    """
    company_id = models.CharField(max_length=255, default=generate_unique_id)
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    continent = models.CharField(max_length=255, default='asia')
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    popularity = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    qualification = models.IntegerField(default=0)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    objects = CompanyManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Company, self).save(*args, **kwargs)
    
    def can_buy_landscape(self, landscape: app.models.Landscape) -> bool:
        """
        Return true if the company can buy the given landscape
        """
        return self.balance >= landscape.buy_cost
    

    def purchase_landscape(self, landscape: app.models.Landscape) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        This function does not call company_able_to_purchase_method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(landscape, app.models.Landscape):
            self.balance -= landscape.buy_cost
            if self.balance < 0:
                raise ValueError("Company balance must be positive")
            else:
                landscape.company = self
                landscape.company_name = self.company_name
                self.save()
                landscape.buy()
        else:
            raise TypeError("The landscape param must be an instance of landscape but "
                            "got {} instead".format(type(landscape)))
