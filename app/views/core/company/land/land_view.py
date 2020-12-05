from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from app.models.company.land_own import LandOwn
import random

class LandAvailable(View):
    template_name = 'core/land/all.html'
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            lands_available = LandOwn.objects.get_available_land()
            random_lands = random.sample(list(lands_available.values()), 5)
            return JsonResponse(random_lands, safe=False)
        data = {'error': 'not logged in', 'redirect_url': '/login/'}
        return
