import re
class Validator(object):
    def email_validator(self, email: str) -> bool:
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)