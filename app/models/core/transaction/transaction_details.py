from django.db import models
from app.models.core.transaction import Transaction


class TransactionDetails(models.Model):
    """Each transaction details responsible for managing ONLY ONE type of product"""
    payment_id = models.IntegerField()  # index (pk) key linked to transaction table
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction")
    product_id = models.IntegerField()  # index (pk) key
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=4)  # price per unit
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    money = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)


class TransactionItem(models.Model):
    """The produced item that belongs to given transaction"""
    pass