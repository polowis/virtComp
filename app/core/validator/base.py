import re
class Validator(object):

    @staticmethod
    def is_email(email: str) -> bool:
        """Return true if valid email expression"""
        if isinstance(email, str):
            return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None
        return False

    @staticmethod
    def is_alpha(string: str) -> bool:
        if isinstance(string, str):
            return re.match(r"(^[a-zA-Z])*$", string) != None
            
    @staticmethod
    def is_alphanumeric(string: str) -> bool:
        """return true if given string only contains alphanumeric"""
        if isinstance(string, str):
            return re.match(r"(^[a-zA-Z0-9]*$)", string) != None
        return False
    
    @staticmethod
    def is_boolean(string: str) -> bool:
        if isinstance(string, str):
            return string.lower() in ['true', 'false', '1', '0']

        if isinstance(string, bool):
            return True
        
        return False


    