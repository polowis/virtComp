from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core.building import Building
from app.models.constants import Item
from django.utils import timezone
from django.db.models import Count


class ProductStoredManager(models.Manager):
    def deposit(self, product: Item, building: Building, quantity: int):
        """Deposit a product with given quantity in given building
        
        This method will try to deposit a product into the database but with stacks
        each stach can only hold 99 items per one type.

        If the quantity provided exceed the remaining space left in the stack, it will
        automatically create a new stack. If item does not exist, it will also create another one
        with each stack holding 99 items.
        """
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
    
    def withdraw(self, product: Item, building: Building, quantity: int, building_transfer: Building):
        """
        Withdraw the product with the given quantity from the given building
        
        This method does somewhat different things than deposit process. First it will try to withdraw
        the item with given quantity from the storage. Next, it will have to rearrage the storage so that only
        one stack with missing quantity is remaining. THERE CANNOT BE 2 STACKS WITH LESS THAN 99 ITEMS.

        The withdraw process will needs to take into account of the location where to store the item after withdraw
        If you are looking for a method to withdraw then transfer to a shop to sell. Consider using ProductSale model
        """
        # first check if product exists
        if self.product_exists(product, building) and quantity <= self.total_quantity(product, building, quantity):
            total_valid_quantity = quantity
            if quantity < 99:
                # get the product where the number of item is less than 99
                try:
                    product: ProductStored = self.get(name=product.name, building=building, quantity__lt=99)
                    product.withdraw(quantity)
                except ProductStored.DoesNotExist:
                    # if the product does not exist, in this case, it means that the quantity of all items
                    # are fully filled up to 99. We just take the first stack
                    product: ProductStored = self.filter(name=product.name, building=building).first()
                    product.withdraw(quantity)
            else:
                #  if required quantity larger than 99
                products = self.filter(name=product.name, building=building)
                for product in products:
                    if product.quantity - quantity < 0:  # if the quantity is larger than the product quantity
                        product.withdraw(99)  # withdraw 99 and delete the object
                        quantity -= 99
                    else:
                        product.withdraw(quantity)
                    
            self.deposit(product, building_transfer, total_valid_quantity)
    
    def create_fresh_product(self, product: Item, building: Building, quantity: int) -> None:
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
    
    def product_exists(self, product: Item, building: Building):
        """Check if the product exists in the given building storage"""
        # use filter method here because we will retrieve multiple products
        return self.filter(product=product, building=building).exists()
    
    def total_quantity(self, product: Item, building: Building):
        """Return the total quantity of the given product in the given building"""
        return self.filter(product=product, building=building).aggregate(Count('quantity'))



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
    
    def withdraw(self, quantity: int) -> None:
        """Withdraw the item with given quantity, if quantity drops below 0
        The object get destroyed automatically.
        """
        self.quantity -= quantity
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()