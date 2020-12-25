from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True)

    @property
    def details(self):
        """return the details of given transaction"""
        return self.transactiondetails_set.all()