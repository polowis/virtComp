from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.core.util.base import generate_unique_id
import logging
from app.models import Landscape

logger = logging.getLogger(__name__)


class CompanyManager(models.Manager):
    def create_company(self, company_name, owner_name, owner_object):
        company = self.create(company_name=company_name, owner_name=owner_name,
                              owner=owner_object)
        return company

    def company_is_exists(self, name: str) -> bool:
        """Return true if company exists"""
        try:
            self.get(company_name=name)
            return True
        except Exception as e:
            logger.warn(e)
            return False


class Company(models.Model):
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
    
    def can_buy_landscape(self, landscape: Landscape) -> bool:
        """
        Return true if the company can buy the given landscape
        """
        if type(landscape) == Landscape:
            return self.balance >= landscape.buy_cost
