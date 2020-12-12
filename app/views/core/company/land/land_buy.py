from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from app.models import LandOwn, Company
from app.core.util.company import get_current_register_company

class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: LandOwn = LandOwn.objects.get(land_id=land_id)
            company: Company = get_current_register_company(request)
            if land.company_name is not None:
                self.buy(land, company)
            else:
                data = {'error': True, 'message': "A company has owned this land"}
                return JsonResponse(data)
        except:
            data = {'error': True, 'message': 'Not found'}
            return JsonResponse(data)
    

    def buy(self, land: LandOwn, company: Company):
        if company.balance >= land.buy_cost:
            new_balance = company.balance - land.buy_cost
            company.balance = new_balance
            company.save()