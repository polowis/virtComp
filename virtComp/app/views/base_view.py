from django.http import HttpResponse
from django.template import loader

class BaseView(object):
    def index(self, request):
        view = loader.get_template("")
        return HttpResponse("Hello")