from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape
import random
from setting import local_settings as env
from app.core.mixin.base import CompanyLoggedInRequiredMixinJSON


class LandscapeBrowse(View, CompanyLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/landscape/browse/

    SUPPORT_METHOD: ['GET']

    HELP: Get random list of landscape that are not belong to any company

    PERMISSION: Company logged in

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            lands_available = Landscape.objects.get_available_land()
            random_lands = random.sample(list(lands_available.values()), env.MAXIMUM_lAND_VIEW)
            return JsonResponse(random_lands, safe=False)
        data = {'error': True, 'message': 'Auth Error', 'redirect_url': '/login/'}
        return JsonResponse(data, safe=False)