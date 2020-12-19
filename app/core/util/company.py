from django.http import HttpRequest
from app.models.core import Company
from typing import Union


def get_current_register_company(request: HttpRequest, *args, **kwargs) -> Union[Company, None]:
    """Return the company instance or None if no company found.
    
    This function will take the HttpRequest instance as param

    It will looked for signed cookie with the name of host_user and
    ONLY return Company instance if and only if that company exists and belongs to
    the requested user
    """

    if request.user.is_authenticated:
        cookie_name = 'host_user'
        cookie = request.get_signed_cookie(cookie_name)
        if cookie is not None:
            try:
                company = Company.objects.get(company_name=cookie)
                if company.owner_name == request.user.username:
                    return company
                return None
            except Exception as e:
                return None
        return None
    return None

