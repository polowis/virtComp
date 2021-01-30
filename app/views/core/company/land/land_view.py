from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from app.models import Landscape
import random

from setting import local_settings as env
from app.core.mixin.base import *
import logging
from django.http import Http404

logger = logging.getLogger(__name__)


class LandAvailable(CompanyLoggedInRequiredMixin, View):
    """
    Return view and the list of available lands that are not owned by any company

    support methods: ['get', 'post']
    """
    template_name = 'core/land/all.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('/login/')

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            lands_available = Landscape.objects.get_available_land()
            random_lands = random.sample(list(lands_available.values()), env.MAXIMUM_lAND_VIEW)
            return JsonResponse(random_lands, safe=False)
        data = {'error': 'not logged in', 'redirect_url': '/login/'}
        return JsonResponse(data, safe=False)


class LandView(UserLoggedInRequiredMixin, View):
    """
    Responsible for display view for land/land_id/view
    
    support methods: ['get', 'post']
    """
    template_name = 'core/land/view.html'

    def get(self, request: HttpRequest, land_id=None):
        if land_id is None:
            raise Http404()
        try:
            Landscape.objects.get_landscape_as_dict(land_id)
            return render(request, self.template_name)
        except Exception as e:
            logger.warn(e)
            raise Http404()

    def post(self, request: HttpRequest, land_id=None):
        try:
            land = Landscape.objects.get_landscape_as_dict(land_id)
            return JsonResponse(land, safe=False)
        except Exception as e:
            logger.warn(e)
            data = {'error': 'Not Found'}
            return JsonResponse(data)


class LandCompanyView(View):
    """Retrieve all the lands from signed company in cookie.

    THIS IS NOT API.
    
    route: company/land/all
    support methods: ['get', 'post']
    """
    template_name = 'core/company/lands.html'

    def post(self, request: HttpRequest):
        company: Company = request.company
        if company is not None:
            landscapes = Landscape.objects.get_landscape_by_company(company, force_json=True)
            return JsonResponse(landscapes, safe=False)
    
    def get(self, request: HttpRequest):
        return render(request, self.template_name)
