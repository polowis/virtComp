
from django.http import HttpRequest, HttpResponse, JsonResponse
from app.core.util.company import *
from django.core.exceptions import PermissionDenied

class CompanyLoggedInRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        company = get_current_register_company(request)
        if company is not None:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CompanyLoggedInRequiredJSONMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        company = get_current_register_company(request)
        if company is not None:
            return super().dispatch(request, *args, **kwargs)
        else:
            data = {'error': 'No company found'}
            return JsonResponse(data, safe=False)