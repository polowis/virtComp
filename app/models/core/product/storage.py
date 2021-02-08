from django.db import models
from app.models.core.building import Building
from django.utils import timezone
from app.models.core.product import ProducedItem


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
    
    def update_capacity(self):
        capacity = ProducedItem.objects.filter(building=self.building, in_global_store=False).count()
        self.current_capacity += capacity
        self.save()