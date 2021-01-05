from django.db import models
from app.models import Company, Item
from app.core.util.base import generate_unique_id


class ProductAgent(models.Model):
    # the unique id of the product record. NOTE: this is the id of recorded row not the product id itself
    record_id = models.CharField(max_length=255, default=generate_unique_id)

    # cost per unit
    price = models.DecimalField(max_digits=20, decimal_places=4)

    # the number of products in this group
    quantity = models.IntegerField()

    # the discount number must be a decimal number and must not has percentage sign
    # example: convert 10% -> 0.1
    # supported discount per product.
    discount = models.DecimalField(max_digits=20, decimal_places=4)

    # the products name
    name = models.CharField(max_length=255)
    item_object = models.ForeignKey(Item, on_delete=models.CASCADE)

    # the company in which this product belongs to
    company_name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)

    # the bought at field does not indicate the time at which the users make the purchase but the time
    # when this type of product runs out, limit to 99 products per record
    bought_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)