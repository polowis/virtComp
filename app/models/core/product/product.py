from django.db import models
from app.models.core import Company
from django.utils import timezone
from app.core.util.base import generate_unique_id
from app.models.constants import Item


class ProductManager(models.Manager):
    def create_product(self, item: Item, quantity: int, price: float, company: Company):
        pass

    def get_product_by_id(self, record_id: str):
        """Make sure to catch obj.DoesNotExist exception when calling this method"""
        return self.get(record_id=record_id)


class Product(models.Model):
    """
    The product on sale for purchasing by company
    The produce for agents will be separated from this model.

    The user can post a produce on store but limit to 99 items per product type
    which means if it reaches this number, uses will need to create another product instead

    We also allow users to update the product quantity so they do not have to create a new one again

    NOTE: this is for sale purpose. To store purpose, please see ProductStored model instead.
    """

    # the unique id of the product record. NOTE: this is the id of recorded row not the product id itself
    record_id = models.CharField(max_length=255, default=generate_unique_id)

    # cost per unit
    price = models.DecimalField(max_digits=20, decimal_places=4)

    # the number of products in this group
    quantity = models.DecimalField(max_digits=20, decimal_places=4)

    # the discount number must be a decimal number and must not has percentage sign
    # example: convert 10% -> 0.1
    # supported discount per product.
    discount = models.DecimalField(max_digits=20, decimal_places=4)

    # the products name
    name = models.CharField(max_length=255)
    item_object = models.ForeignKey()

    # the company in which this product belongs to
    company_name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)

    # the bought at field does not indicate the time at which the users make the purchase but the time
    # when this type of product runs out, limit to 99 products per record
    bought_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    objects = ProductManager()


    def save(self, *args, **kwargs):
        """Save this object to database"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def buy(self, company: Company, quantity: int):
        """The function to buy the product"""
        quantity: int = int(quantity)  # try to convert to integer type when neccessary
        if isinstance(company, Company):  # explicit type check to prevent further error
            # check if the request to buy product lower or equal to available number of products left
            if quantity <= self.quantity:
                total_cost = quantity * self.price
                # if company does not have enough money to buy (result in 0)
                if company.balance - total_cost < 0:
                    raise TypeError("Company balance cannot be negative number")
                company.balance = company.balance - total_cost
                company.save()
                self.quantity = self.quantity - quantity
                if self.quantity == 0:
                    self.bought_at = timezone.now()
    
    def update_quantity(self, company: Company, quantity: int):
        """Update the quantity of this product

        algorithm as follow: check if the number of this type of product
        that the requested company owns matches the number of product the requested
        company wants to put on sale.

        Check if requested company owns this product
        The requested company can withdraw this product. If the quantity reaches 0, this recorded
        will be destroyed. Update the deleted_at field not the bought_at field

        To know whether the item will be withdrawed or added. the number of quantity will tell
        if it increases -> adding. else withdrawing. If withdrawing, it needs to specify the storage object to store
        items. if none is specify, the method will choose the first storage object in the list raise error if that 
        storage does not have enough space
        """
        pass
    
    def update_price(self, company: Company):
        """
        Update the product price. If this products is owned by the requested company
        """
        pass
