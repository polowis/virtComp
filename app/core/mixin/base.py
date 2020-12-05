
from django.http import HttpRequest, HttpResponse, JsonResponse
from app.core.util.company import *

class CompanyLoggedInRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        company = get_current_register_company(request)
        if company is not None:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(status=404)


class CompanyLoggedInRequiredJSONMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        company = get_current_register_company(request)
        if company is not None:
            return super().dispatch(request, *args, **kwargs)
        else:
            data = {'error': 'No company found'}
            return JsonResponse(data, safe=False)
