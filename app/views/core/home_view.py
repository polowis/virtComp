from django.views import View
from django.http import HttpRequest
from django.shortcuts import render, redirect

class HomeView(View):
    template_name = "core/home.html"
    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return redirect("/login")
        return render(request, self.template_name)


