from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core.building import Building
from app.models.constants import Item
from django.utils import timezone
from django.db.models import Count


class ProducedItemManager(models.Manager):
    def create_produced_item(self, product: Item, building: Building, quality: float):
        """Store the item in building storage"""
        self.create(name=product.name, building=building, item=product, quality=quality)
        
    def filter_product_by_quality(self, product: Item, building: Building, quality_start, quality_end):
        return self.filter(item=product, building=building, quality__range=[quality_start, quality_end])

    def product_exists(self, product: Item, building: Building):
        """Check if the product exists in the given building storage"""
        # use filter method here because we will retrieve multiple products
        return self.filter(product=product, building=building).exists()
    
    def total_quantity(self, product: Item, building: Building):
        """Return the total quantity of the given product in the given building"""
        return self.filter(product=product, building=building).aggregate(Count('quantity'))



class ProducedItem(models.Model):
    """The products stored in each building"""
    record_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)  # the storage that holds the item
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # the constant item attribute
    quality = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    objects = ProducedItemManager()

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def withdraw(self, quantity: int) -> None:
        """Withdraw the item with given quantity, if quantity drops below 0
        The object get destroyed automatically.
        """
        self.quantity -= quantity
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()