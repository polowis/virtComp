from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape, Company
from app.core.util.company import get_current_register_company
import logging

logger = logging.getLogger(__name__)


class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)
            company: Company = request.company
            print(company)
            if land.can_be_purchased() and company is not None:
                if company.can_buy_landscape(land):
                    company.purchase_landscape(land)
                    if land.company_name == company.company_name:
                        data = {'error': True, 'message': 'Successfully Purchase Landscape',
                                'redirect_url': '/company/'}
                        return JsonResponse(data)
            else:
                data = {'error': True, 'message': "A company has owned this land"}
                return JsonResponse(data)
        except Exception as e:
            logger.warn(e)
            data = {'error': True, 'message': 'Not found'}
            return JsonResponse(data)
    

    def buy(self, land: Landscape, company: Company):
        if company.balance >= land.buy_cost:
            new_balance = company.balance - land.buy_cost
            company.balance = new_balance
            company.save()