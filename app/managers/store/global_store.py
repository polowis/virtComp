import app.models.core.store as store
import app.models.core.product as product
from django.db import models


class GlobalStoreItemManager(models.Manager):
    def _store_item(self, item: product.ProducedItem, price, company_storage: store.GlobalStore):
        """
        Store item in the global store

        :param item: ProducedItem instance
        :param price: Price of the item
        :param company_storage: GlobalStore instance
        """
        try:
            self.get(produced_item_id=item.id)
            raise self.model.AlreadyExists()
        except self.model.DoesNotExist:
            return self.create(produced_item_id=item.id, produced_item=item,
                               price=price, company_store=company_storage)