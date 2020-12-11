from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core.signing import Signer

class CompanyLoggedInView(View):
    def post(self, request: HttpRequest):
        company_name = request.POST.get('companyName', None)
        if company_name is not None:
            data = {'success': True, 'redirect_url': '/company/'}
            json_response = JsonResponse(data)
            http_response = HttpResponse(json_response)
            http_response.set_signed_cookie('host_user', company_name)
            return http_response
        data = {'error': True}
        return JsonResponse(data)
