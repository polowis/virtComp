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
            return JsonResponse(land.as_dict())
        except Exception:
            data = {'error': True, 'message': 'Landscape not found'}
            return JsonResponse(data)