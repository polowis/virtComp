import re
from django.http import HttpRequest


class UserAgentMiddleware(object):

    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request: HttpRequest):
        request.user_agent = UserAgent(request.META.get('HTTP_USER_AGENT'))



class UserAgent(object):
    def __init__(self, ua_string: str):
        self.user_agent = ua_string

    
    def is_mobile(self):
        pattern = re.compile(r".*(palm|blackberry|nokia|phone|midp|mobi|symbian|chtml|ericsson|minimo|audiovox|motorola|samsung|telit|upg1|windows ce|ucweb|astel|plucker|x320|x240|j2me|sgh|portable|sprint|docomo|kddi|softbank|android|mmp|pdxgw|netfront|xiino|vodafone|portalmmm|sagem|mot-|sie-|ipod|up\\.b|webos|amoi|novarra|cdm|alcatel|pocket|ipad|iphone|mobileexplorer|mobile)", re.IGNORECASE)
        if pattern.match(self.user_agent):
            return True
        return False
    
    def is_pc(self):
        return not self.is_mobile