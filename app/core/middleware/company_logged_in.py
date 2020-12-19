from app.core.util.company import get_current_register_company


class CompanyLoggedInMiddleware(object):
    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        request.company = get_current_register_company(request)
