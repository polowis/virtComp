from django.views import generic, View
from django.http import HttpResponseRedirect
from django.shortcuts import render

class HomeView(View):
    """Index entry"""
    def get(self, request):
        template_name = 'index.html'
        return render(request, self.template_name)