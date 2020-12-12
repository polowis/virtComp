from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core.signing import Signer
from app.models import Company
from typing import Union, List

class CompanyLoggedInView(View):
    def post(self, request: HttpRequest):
        company_name = request.POST.get('companyName', None)
        if company_name is not None:
            data = {'success': True, 'redirect_url': '/company/'}
            json_response = JsonResponse(data)
            http_response = HttpResponse(json_response)
            http_response.set_signed_cookie('host_user', company_name)
            return http_response
        data = {'error': True, 'message': "Parameter name of the company must not be empty"  }
        return JsonResponse(data)
    
    def company_is_exists(self, name: str) -> Union[bool, List]:
        try:
            company: Company = Company.objects.get(company_name=name)
            return True
        except Company.DoesNotExist:
            data = {'error': True, 'message': "Company not found"}
            return data
    
    def user_owns_company(self, company: Company, username) -> bool:
        return company.owner_name == username
