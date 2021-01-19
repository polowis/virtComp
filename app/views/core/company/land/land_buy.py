from django.views import View
from django.http import HttpRequest, JsonResponse, Http404
from app.models import Landscape, Company


class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)
            company: Company = request.company
            if land.can_be_purchased() and company is not None:
                if company.can_own_landscape(land, 'buy'):
                    company.purchase_landscape(land)
                    if land.company_name == company.company_name:
                        data = {'error': False, 'message': 'Successfully Purchase Landscape',
                                'redirect_url': '/company/'}
                        return JsonResponse(data)
                data = {'error': True, 'message': "Insufficient amount of money"}
                return JsonResponse(data)
            data = {'error': True, 'message': "A company has owned this land"}
            return JsonResponse(data)
        except Landscape.DoesNotExist:
            data = {'error': True, 'message': 'Not found'}
            return JsonResponse(data)
    
    def get(self, request: HttpRequest, land_id=None):
        raise Http404()