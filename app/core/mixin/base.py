
from django.http import HttpRequest, JsonResponse
from app.core.util.company import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


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
            data = {'error': True, 'message': 'No company found (404)'}
            return JsonResponse(data, safe=False)


class UserLoggedInRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/login/')


class UserLoggedInRequiredMixinJSON:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            data = {'error': True, 'message': 'User not logged in', 'redirect_url': '/login/'}
            return JsonResponse(data, safe=False)



class RedirectIfLoggedInMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/home/')


class MobileRedirectMixin(object):
    pass
