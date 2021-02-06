from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape
from app.core.mixin.base import CompanyLoggedInRequiredMixinJSON
from app.models import Company


class LandscapeBuy(View, CompanyLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/landscape/{id}/buy/

    SUPPORT_METHOD: ['POST']

    HELP: Buy the landscape of requested id

    PERMISSION: Company logged in

    RETURN: JSON response
    """
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)
            company: Company = request.company
            if land.can_be_purchased() and company is not None:
                if company.can_own_landscape(land, 'buy'):
                    company.buy_landscape(land)
                    if land.company_name == company.company_name:
                        data = {'error': False, 'message': 'Successfully Buy Landscape',
                                'redirect_url': '/company/'}
                    else:
                        data = {'error': False, 'message': 'Failure to Buy Landscape due to unknown reason'}
                data = {'error': True, 'message': "Insufficient amount of money"}
            data = {'error': True, 'message': "A company has owned this land"}
        except Landscape.DoesNotExist:
            data = {'error': True, 'message': 'Not found'}
        return JsonResponse(data)