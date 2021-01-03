from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core.building import Building
from app.models.constants import Item
from django.utils import timezone


class ProductStoredManager(models.Manager):
    def store(self, product: Item, building: Building, quantity: int):
        try:
            # we can only have one stack with less than 99 needs to filled up
            product: ProductStored = self.get(name=product.name, building=building, quantity__lt=99)
            remaining_quantity_needs = 99 - product.quantity
            quantity -= remaining_quantity_needs
            product.store(remaining_quantity_needs)
            if quantity > 0:  # indicate there is still items left
                self.create_fresh_product(product, building, quantity)
        except ProductStored.DoesNotExist:
            self.create_fresh_product(product, building, quantity)
    
    def create_fresh_product(self, product, building, quantity):
        #  quantity input cannot be negative number
        if quantity < 0:
            raise ValueError("The quantity of the product cannot be negative number")
        if quantity <= 99:
            return self.create(name=product.name, building=building, quantity=quantity, item=product)
        if quantity > 99:
            number_of_stack = 0
            remaining_quantity = quantity
            for i in range(0, quantity):
                if i % 98 == 1:  # for every 99 items
                    number_of_stack += 1
            for i in range(number_of_stack):
                self.create(name=product.name, building=building, quantity=99)
                remaining_quantity -= 99
            if remaining_quantity > 0:
                self.create(name=product.name, building=building, quantity=remaining_quantity)



class ProductStored(models.Model):
    """The products stored in each building"""
    record_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def store(self, quantity: int) -> None:
        """Store more item in this stack"""
        self.quantity += quantity
        self.save()