from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from app.models.company.land_own import LandOwn
import random
from setting import local_settings

class LandAvailable(View):
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

class LandView(View):
    template_name = 'core/land/view.html'
    def get(self, request: HttpRequest, land_id=None):
        if land_id is None:
            return HttpResponse(status=404)
        land = get_object_or_404(LandOwn, land_id=land_id)
        return render(request, self.template_name)
