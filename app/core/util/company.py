from django.http import HttpRequest
from app.models.company import Company

def get_current_register_company(request: HttpRequest):
    if request.user.is_authenticated:
        cookie_name = 'company'
        cookie = request.COOKIES.get(cookie_name, None)
        if cookie is not None:
            try:
                company = Company.objects.get(company_name=cookie_name)
                if company.owner_name == request.user.username:
                    return company
                return None
            except:
                return None
        return None
    return None

