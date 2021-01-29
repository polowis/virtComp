from app.models import ProducedItem, Company
from typing import List


class TransactionBuilder(object):
    def __init__(self, from_company: Company, amount: float = 0, item: List[ProducedItem] = None):
        self.amount = amount
        self.item = item
        self.from_company = from_company

    def to_company(self, company: Company):
        """Create a transaction to company"""
        if self._has_enough_money_to_transfer():
            self.from_company.balance -= self.amount
            company.balance += self.amount
            self.from_company.save()
            company.save()

    def to_agent(self):
        pass

    def create_transaction(self):
        pass
    
    def _has_enough_money_to_transfer(self):
        return self.from_company.balance >= self.amount