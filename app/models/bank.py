

from django.db import models


class CommunityBank(models.Model):
    balance = models.DecimalField(max_digits=30, decimal_places=4)



class OwnerBank(models.Model):
    balance = models.DecimalField(max_digits=30, decimal_places=4)