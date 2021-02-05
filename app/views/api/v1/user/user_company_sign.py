from django.views import View
from django.http import JsonResponse, HttpResponse, HttpRequest
from app.models import Company
from app.core.mixin.base import UserLoggedInRequiredMixinJSON


class UserCompanySign(View, UserLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/user/company/sign/

    SUPPORT_METHOD: ['POST']

    HELP: Logged in given company name

    RETURN: JSON response
    """
    def post(self, request: HttpRequest):
        company_name = request.POST.get('companyName', None)
        if company_name is not None and Company.objects.company_exists(company_name):
            company: Company = Company.objects.get(company_name=company_name)
            if company.owned_by(request.user.username):
                data = {'success': True, 'redirect_url': '/company/'}
                json_response = JsonResponse(data)
                http_response = HttpResponse(json_response)
                http_response.set_signed_cookie('host_user', company_name)
                return http_response
        data = {'error': True, 'message': "The name of company is not valid"}
        return JsonResponse(data)