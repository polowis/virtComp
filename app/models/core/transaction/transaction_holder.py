from django.db import models
from app.models.core import Company
from app.models.core.transaction import Transaction


class TransactionHolder(models.Model):
    payment_id = models.IntegerField()
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    sender_id = models.CharField(max_length=255)  # company unique id
    receiver_id = models.CharField(max_length=255)  # company unique id
    seller = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sender")
    buyer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="receiver")
    