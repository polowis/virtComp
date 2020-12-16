
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest


def Error403(request: HttpRequest, exception=None):
    template_name = 'exceptions/403.html'
    template = render_to_string(template_name)
    return HttpResponse(template, status=403)


def Error404(request: HttpRequest, exception=None):
    template_name = 'exceptions/404.html'
    template = render_to_string(template_name)
    return HttpResponse(template, status=404)


def Error500(request: HttpRequest, exception=None):
    template_name = 'exceptions/500.html'
    template = render_to_string(template_name)
    return HttpResponse(template, status=500)