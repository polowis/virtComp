from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app.models.company.land_own import LandOwn
import random
from setting import local_settings
from app.core.mixin.base import *


class LandAvailable(CompanyLoggedInRequiredMixin, View):
    template_name = 'core/land/all.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('/login/')

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            lands_available = LandOwn.objects.get_available_land()
            random_lands = random.sample(list(lands_available.values()), local_settings.MAXIMUM_lAND_VIEW)
            return JsonResponse(random_lands, safe=False)
        data = {'error': 'not logged in', 'redirect_url': '/login/'}
        return JsonResponse(data, safe=False)


class LandView(UserLoggedInRequiredMixin, View):
    template_name = 'core/land/view.html'

    def get(self, request: HttpRequest, land_id=None):
        if land_id is None:
            return HttpResponse(status=404)
        try:
            LandOwn.objects.values().get(land_id=land_id)
            return render(request, self.template_name)
        except Exception as e:
            return HttpResponse(status=404)

    def post(self, request: HttpRequest, land_id=None):
        try:
            land = LandOwn.objects.values().get(land_id=land_id)
            return JsonResponse(land, safe=False)
        except Exception as e:
            data = {'error': 'Not Found'}
            return JsonResponse(data)
