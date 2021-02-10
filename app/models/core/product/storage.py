from django.db import models
from app.models.core.building import Building
from django.utils import timezone
from app.models.core.product import ProducedItem
from typing import List


class StorageManager(models.Manager):
    def create_storage(self, building, max_capacity):
        """Create the storage associated with the given building"""
        return self.create(building=building, max_capacity=max_capacity)


class Storage(models.Model):
    """
    The storage model for handling storage
    """
    building = models.OneToOneField(Building, on_delete=models.CASCADE)
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)
    updated_at = models.DateTimeField()

    objects = StorageManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def add(self, item, quality):
        """Add an item to the storage
        
        :param item: Item instance
        :quality: Quality of the item
        """
        try:
            ProducedItem.objects.create_produced_item(item, self.building, quality)
            self.current_capacity += 1
            self.save()
        except Exception as e:
            raise Exception(e)
    
    def move_to_global_store(self, item):
        pass
    
    def has_item(self, item: str):
        """Check if item exists in the storage"""
        if isinstance(item, str):
            return ProducedItem.objects.filter(name=item, building=self.building).exists()
        return ProducedItem.objects.filter(item=item, building=self.building).exists()
    
    def get_item(self, item: str):
        """
        Get all item by name belongs to this building storage
        """
        if isinstance(item, str):
            return ProducedItem.objects.filter(name=item, building=self.building)
        return ProducedItem.objects.filter(name=item, building=self.building)
    
    def update_capacity(self, current_capacity: int = None):
        """Update the current capacity of the storage
        But not recommended to use this method since it will try to count all the items in
        the storage which might result in low performance.
        """
        if current_capacity is not None:
            self.current_capacity = current_capacity
            return
        
        # we only count those item that are not in the global store
        capacity = ProducedItem.objects.filter(building=self.building, in_global_store=False).count()
        self.current_capacity += capacity
        self.save()
    
    def _reaches_max_capacity(self, current_capacity: int = None) -> bool:
        """
        Return True if the storage reach the max_capacity given the current capacity
        """
        if current_capacity is None:
            current_capacity = self.current_capacity
        return current_capacity > self.max_capacity

    def put_item_back_to_storage(self, items: List[ProducedItem]):
        """If the item is already in the global store, put it back to storage
        But watch for capacity might reach max capacity.
        """
        items_length = len(items)
        # only loop for
        items = items[1:items_length]
        items_id = [item.id for item in items]
        ProducedItem.objects.filter(id__in=items_id).update(in_global_store=False)
        self.current_capacity += items_length
        self.save()