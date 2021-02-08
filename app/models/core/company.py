from __future__ import annotations
import app.models
from django.db import models
from django.utils import timezone
from .user import User
from app.core.util.base import generate_unique_id
from app.core.validator.base import Validator
import logging
from app.models.constants import Land
from app.models.core.exception import UnableToAssignEmployee
from typing import Union
from app.core.db import ModelMixin
logger = logging.getLogger(__name__)


class CompanyManager(models.Manager):
    def create_company(self, company_name: str, owner_object: User,
                       continent: str = Land.objects.default_continent()) -> Company:
        """Create a company and save them to database. Return Company object.

        This method does not check for validity. Please call can_create_company method before this

        :param company_name: Name of the company

        :param owner_object: The user object

        :continent: the continent of the company

        throw exception if unable to create
        """
        if self.can_create_company(company_name, continent):
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
    
    def can_create_company(self, company_name: str, continent: str) -> bool:
        """Return true if the given company can be created
        
        This will ensure that the company name has not been registered and has a valid name
        """
        if company_name is None or continent is None:
            return False
        return (not self.company_exists(company_name)
                and self.has_valid_company_name(company_name)  # noqa
                and continent.lower() in Land.objects.get_supported_continents())  # noqa


class Company(models.Model, ModelMixin):
    """
    The company model. Use this class if you want to create a company associated with given user
    """
    company_id = models.CharField(max_length=255, default=generate_unique_id)
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    continent = models.CharField(max_length=255, default=Land.objects.default_continent())
    balance = models.DecimalField(default=300, max_digits=20, decimal_places=4)
    popularity = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    qualification = models.IntegerField(default=0)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    objects = CompanyManager()

    protected = ['created_at', 'updated_at', 'deleted_at']

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Company, self).save(*args, **kwargs)
    
    def can_own_landscape(self, landscape: app.models.Landscape, method_acquired: str) -> bool:
        """
        Return true if the company can buy / rent the given landscape

        This is the function to own the given landscape. Alternatively, consider using
        Landscape.company_able_to_purchase() method instead

        :param: Landscape

        :method_acquired: supported_methods_acquired ['buy', 'rent', 'buy_cost', 'rent_cost']
        """

        supported_methods_acquired = ['buy', 'rent', 'buy_cost', 'rent_cost']
        if method_acquired.lower() in supported_methods_acquired and isinstance(method_acquired, str):
            if not method_acquired.lower().endswith('_cost'):
                method_acquired = method_acquired.lower() + '_cost'
            
            if type(landscape) == app.models.Landscape:
                return self.balance >= getattr(landscape, method_acquired)
        raise TypeError("method_acquired param must be in supported methods but got %s instead" % method_acquired)
    
    def purchase_landscape(self, landscape: app.models.Landscape) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        DEPRECATED: Use buy_landscape() instead for better naming.

        This function does not call can_buy_landscape method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(landscape, app.models.Landscape):
            if self._does_not_have_enough_money(landscape.buy_cost):
                raise ValueError("Company does not have enough money")
            else:
                self.balance -= landscape.buy_cost
                landscape.company = self
                landscape.company_name = self.company_name
                self.save()
                landscape.buy()
        else:
            raise TypeError("The landscape param must be an instance of landscape but "
                            "got {} instead".format(type(landscape)))
    
    def buy_landscape(self, landscape: app.models.Landscape) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        This function does not call can_buy_landscape method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(landscape, app.models.Landscape):
            if self._does_not_have_enough_money(landscape.buy_cost):
                raise ValueError("Company does not have enough money")
            else:
                self.balance -= landscape.buy_cost
                landscape.company = self
                landscape.company_name = self.company_name
                self.save()
                landscape.buy()
        else:
            raise TypeError("The landscape param must be an instance of landscape but "
                            "got {} instead".format(type(landscape)))
    
    def rent_landscape(self, landscape: app.models.Landscape) -> None:
        """The function will withdraw a certain amount of money from given company
        
        :param company: The company instance that wish to own this landscape

        This function does not call can_buy_landscape method, you must call it manually and before this function
        or else an exception will be thrown
        """
        if isinstance(landscape, app.models.Landscape):
            if self._does_not_have_enough_money(landscape.rent_cost):
                raise ValueError("Company does not have enough money")
            else:
                self.balance -= landscape.rent_cost
                landscape.company = self
                landscape.company_name = self.company_name
                self.save()
                landscape.rent()
        else:
            raise TypeError("The landscape param must be an instance of landscape but "
                            "got {} instead".format(type(landscape)))
    
    def hire(self, agent):
        """Hire the given agent.
        The agent will be assigned to the company but however not distributed to building
        If the agent has not distributed to any building, the agent will not be able to earn money

        Make sure to call Company.distribute() method directly.
        """
        agent.company_name = self.company_name
        agent.save()
        return
    
    def distribute(self, agent, building) -> None:
        """
        Distribute the agent to building

        TODO: Check for maximum employees
        """
        if building.company_name == self.company_name:  # check if building is owned by the company
            if agent.company_name == self.company_name:  # check if agent in this company
                agent.building = building
                agent.save()
                return
        raise UnableToAssignEmployee()

    def fire(self, agent) -> None:
        """
        Fire the given agent out of the company
        """
        agent.company_name = None
        agent.building = None
        agent.save()
    
    def _does_not_have_enough_money(self, expected_amount: Union[float, int]) -> bool:
        """
        Return true if the company does not have enough money matching the expected amount
        """
        return self.balance < expected_amount
    
    def construct_building(self):
        pass

    def get_all_buildings(self):
        """"""
        return self.building_set.all()
    
    def get_all_landscape(self):
        return self.landscape_set.all()
    
    def owned_by(self, username: str) -> bool:
        """
        Return true if the company owns by the given username

        :param username: string

        :return boolean
        """
        return self.owner_name == username
    
    def pay(self, amount: Union[int, float]) -> None:
        self.balance -= amount
        self.save()
        

