from django.db import models
from app.models.constants import Item
from ..building import Building
from django.utils import timezone
import datetime


class ProductProducingManager(models.Manager):
    """The producing process manager"""
    def create_proccess(self, item: Item, expected_quality: float, time: int):
        """Create the producing process for the given item"""
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(seconds=time)
        item_name = item.name
        self.create(name=item_name, item=item, expected_quality=expected_quality, start_time=start_time,
                    end_time=end_time)



class ProductProducing(models.Model):
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    # the building where the process started
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    # the is_success field will be updated as soon as the time is finished
    is_success = models.BooleanField(null=True)
    is_completed = models.BooleanField(null=True)
    expected_quality = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = ProductProducingManager()

    def is_finished(self):
        return self.is_completed or timezone.now() > self.end_time
    
    def move_to(self, building):
        """This function will be used to move the item into storage after
        finishing
        """
        pass