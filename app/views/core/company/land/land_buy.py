from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from app.models import LandOwn, Company
from app.core.util.company import get_current_register_company

class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: LandOwn = LandOwn.objects.get(land_id=land_id)
            company: Company = get_current_register_company(request)
            if company.balance >= land.buy_cost:
                new_balance = company.balance - land.buy_cost
                company.balance = new_balance
                company.save()
        except:
            data = {'error': 'Not Found'}
            return JsonResponse(data)