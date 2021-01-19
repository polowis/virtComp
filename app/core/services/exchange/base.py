from app.models import Continent
from app.models.core.transaction import AgentTransaction


class ExchangeSystem(object):
    def __init__(self, continent):
        self.continent: Continent = Continent.objects.get(name=continent)

    def exchange(self, _from, _to):
        pass
    
    def get(self, continent):
        Continent.objects.get_gdp_per_capita(continent)
    
    def cpi(self, continent):
        k = AgentTransaction.objects.get_total_income(continent)
        if self.continent.cpi is None:
            cpi = k / k * 100
        else:
            pass
        return self.update_continent_cpi(cpi)

    def update_continent_cpi(self, new_cpi):
        self.continent.update_cpi(new_cpi)
        