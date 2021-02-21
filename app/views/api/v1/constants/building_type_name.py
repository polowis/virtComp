from django.http import HttpRequest, JsonResponse
from app.models.constants import BuildingType
from django.views import View
from app.core.mixin.base import CompanyLoggedInRequiredJSONMixin


class BuildingTypeName(View, CompanyLoggedInRequiredJSONMixin):
    """

    URL: api/v1/constants/buildingtypename

    SUPPORT_METHOD: ['GET']

    HELP: Retrieve all the supported building type name

    PERMISSION: company logged in

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        building_type = list(BuildingType.objects.all().values('name'))
        return JsonResponse(building_type, safe=False)
