from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from app.models.company import Company
from app.core.mixin.base import UserLoggedInRequiredMixin

class HomeView(UserLoggedInRequiredMixin, View):
    
    template_name = "core/home.html"

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return redirect("/login/")
        return render(request, self.template_name)


class CurrentUserCompany(View):
    def post(self, request: HttpRequest):
        company = list(Company.objects.filter(owner_name=request.user.username).values())
        return JsonResponse(company, safe=False)




