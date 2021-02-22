from django.views import View
from django.http import HttpRequest
from django.shortcuts import render, redirect
from app.core.mixin.base import CompanyLoggedInRequiredMixin
from app.models import Landscape
from django.http import Http404


class BuildingCreate(View, CompanyLoggedInRequiredMixin):
    template_name = 'core/building/building_create.html'

    def get(self, request: HttpRequest, land_id=None):
        try:
            land: Landscape = Landscape.objects.get(land_id=land_id)  # check if requested land exists
            if land.owned_by(request.company):
                return render(request, self.template_name)
            return redirect(f'/land/{land_id}/view/')
        except Landscape.DoesNotExist:
            raise Http404()