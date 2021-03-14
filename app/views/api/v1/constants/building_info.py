from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import BuildingType
from app.models.core.exception import NegativeLevel


class BuildingInfo(View):
    """
    
    """
    def get(self, request: HttpRequest):
        building_request = request.GET.get("building")
        building_method = request.GET.get("method", "")
        building_level = int(request.GET.get("level", 1))

        try:
            building: BuildingType = BuildingType.objects.get_building_by_type(building_request)
            building_details = {}
            building_details['buildingName'] = building.name
            building_details['cost'] = building.get_cost(building_method.lower(), building_level)

            return JsonResponse(building_details)

        except BuildingType.DoesNotExist:
            data = {'error': True, 'message': 'Building not found'}
            return JsonResponse(data)

        except NegativeLevel:
            data = {'error': True, 'message': 'Unable to view info, requested params might be uncorrect'}
            return JsonResponse(data)