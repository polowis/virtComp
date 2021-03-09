from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import BuildingType


class BuildingInfo(View):
    def get(self, request: HttpRequest):
        building_request = request.GET.get("building")
        try:
            building: BuildingType = BuildingType.objects.get_building_by_type(building_request)
            building_details = building.as_dict()
            print(building_details)
        except BuildingType.DoesNotExist:
            data = {'error': True, 'message': 'Building not found'}
            return JsonResponse(data)