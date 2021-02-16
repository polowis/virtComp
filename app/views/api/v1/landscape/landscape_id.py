from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape
from app.core.mixin.base import CompanyLoggedInRequiredMixinJSON


class LandscapeID(View, CompanyLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/landscape/{id}/

    SUPPORT_METHOD: ['GET']

    HELP: Return landscape information for given id. The id here must be the custom landscape id,
    not the primary_key (auto_increament)

    PERMISSION: Company logged in

    RETURN: JSON response
    """
    def get(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)
            land_details = land.as_dict()
            if land_details['company_name'] == request.company.company_name:
                land_details['owner'] = 1
                land_details['rent_due'] = land.next_pay_rent_date()
            return JsonResponse(land_details)
        except Exception:
            data = {'error': True, 'message': 'Landscape not found'}
            return JsonResponse(data)