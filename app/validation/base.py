from django.http import HttpRequest
from typing import Dict, Optional


class Validation(object):
    def __init__(self, request: HttpRequest, context: Dict[str, str], *arg, **kwargs):
        self.request = request
        self.context = context
    
    def get_context_keys_as_list(self) -> list:
        return list(self.context.keys())
    
    def get_validator_name_as_list(self) -> list:
        return list(self.context.values())
    
    def get_matching_validator_by_key(self, key: str) -> Optional[str]:
        return self.context.get(key, None)