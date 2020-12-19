from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app.models import Landscape
import random
import os
if os.environ.get('GITHUB_WORKFLOW'):
    from setting import settings as env
else:
    from setting import local_settings as env
from app.core.mixin.base import *
import logging

logger = logging.getLogger(__name__)


class LandAvailable(CompanyLoggedInRequiredMixin, View):
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
    template_name = 'core/land/view.html'

    def get(self, request: HttpRequest, land_id=None):
        if land_id is None:
            return HttpResponse(status=404)
        try:
            Landscape.objects.values().get(land_id=land_id)
            return render(request, self.template_name)
        except Exception as e:
            logger.warn(e)
            return HttpResponse(status=404)

    def post(self, request: HttpRequest, land_id=None):
        try:
            land = Landscape.objects.values().get(land_id=land_id)
            return JsonResponse(land, safe=False)
        except Exception as e:
            logger.warn(e)
            data = {'error': 'Not Found'}
            return JsonResponse(data)
