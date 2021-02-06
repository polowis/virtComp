from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape
from app.core.mixin.base import CompanyLoggedInRequiredMixinJSON


class LandscapeView(View, CompanyLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/landscape/

    SUPPORT_METHOD: ['GET']

    HELP: All landscape belongs to given company

    PERMISSION: company logged in

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        landscapes = list(Landscape.objects.filter(company_name=request.company.company_name).values())
        return JsonResponse(landscapes)