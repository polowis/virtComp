from django.db import models
from app.models.core import Company
from app.models.core.product import ProducedItem
from django.utils import timezone

__all__ = ['GlobalStore', 'GlobalStoreItem']


class GlobalStoreManager(models.Manager):
    def register(self, company: Company):
        """
        Register the company to global store.

        :param company: Company instance to register.

        Return the GlobalStore instance
        """
        try:
            self.get(company_name=company.company_name, company=company)
            raise self.model.CompanyAlreadyRegistered()
        except self.model.DoesNotExist:
            return self.create(company_name=company.company_name, company=company)


class GlobalStore(models.Model):
    company_name = models.CharField(max_length=255)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    number_of_products = models.PositiveIntegerField(default=0)
    max_number_of_products = models.PositiveIntegerField(default=2000)

    registered_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField()

    objects = GlobalStoreManager()

    class CompanyAlreadyRegistered(Exception):
        pass

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def put_item_on_store(self, item: ProducedItem, price):
        """Put item on store"""
        return GlobalStoreItem.objects._store_item(item, price, self)


class GlobalStoreItemManager(models.Manager):
    def _store_item(self, item: ProducedItem, price, company_storage: GlobalStore):
        try:
            self.get(item_id=item.id)
            raise self.model.AlreadyExists()
        except self.model.DoesNotExist:
            return self.create(item_id=item.id, produced_item=item,
                               price=price, company_store=company_storage)


class GlobalStoreItem(models.Model):
    item_id = models.IntegerField()
    produced_item = models.OneToOneField(ProducedItem, on_delete=models.CASCADE)
    company_store = models.ForeignKey(GlobalStore, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    is_bought = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    objects = GlobalStoreItemManager()

    class AlreadyExists(Exception):
        pass

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)



