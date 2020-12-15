from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.core.util.base import generate_unique_id


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
