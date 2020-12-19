from django.views import View
from django.shortcuts import render


class HomeView(View):
    """Index entry"""
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)