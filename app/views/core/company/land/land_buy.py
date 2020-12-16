from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape, Company
from app.core.util.company import get_current_register_company


class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)
            company: Company = get_current_register_company(request)
            if not self.land_already_bought(land):
                self.buy(land, company)
            else:
                data = {'error': True, 'message': "A company has owned this land"}
                return JsonResponse(data)
        except:
            data = {'error': True, 'message': 'Not found'}
            return JsonResponse(data)
    

    def buy(self, land: Landscape, company: Company):
        if company.balance >= land.buy_cost:
            new_balance = company.balance - land.buy_cost
            company.balance = new_balance
            company.save()
    
    def land_already_bought(self, land: Landscape) -> bool:
        return land.company_name is not None