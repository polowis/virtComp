from django.views import View
from django.http import HttpRequest, JsonResponse
from app.core.mixin.base import CompanyLoggedInRequiredMixinJSON
from app.core.services.builders.building_builder import BuildingBuilder
from app.models import Landscape
from app.models.core.exception import UnableToConstructBuilding


class BuildingCreate(View, CompanyLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/building/

    SUPPORT_METHOD: ['GET']

    HELP: All landscape belongs to given company

    PERMISSION: company logged in

    RETURN: JSON response
    """
    def post(self, request: HttpRequest, land_id):
        building_level = request.POST.get("level", 1)
        building_type = request.POST.get("buildingType", None)
        building_name = request.POST.get("buildingName", None)
        method = request.POST.get("method", None)

        try:
            landscape: Landscape = Landscape.objects.get(land_id=land_id)

        except Landscape.DoesNotExist:
            data = {'error': True, 'message': 'Land id not found'}
            return JsonResponse(data)
        
        builder = BuildingBuilder(landscape, building_level, building_type, building_name)
        try:
            builder.construct_building(request.company, method)
        except UnableToConstructBuilding:
            data = {'error': True, 'message': 'Error occured while constructing building'}
            return JsonResponse(data)
