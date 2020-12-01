import re
class Validator(object):

    @staticmethod
    def is_email(email: str) -> bool:
        """Return true if valid email expression"""
        if isinstance(email, str):
            return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None
        return False

    @staticmethod
    def is_alpha(context: str) -> bool:
        if isinstance(context, str):
            return re.match(r"(^[a-zA-Z])*$", context) != None
        return False

    @staticmethod
    def is_alphanumeric(context: str) -> bool:
        """return true if given context only contains alphanumeric"""
        if isinstance(context, str):
            return re.match(r"(^[a-zA-Z0-9]*$)", context) != None
        return False
    
    @staticmethod
    def is_number(context):
        if isinstance(context, int):
            return True
        
        if isinstance(context, str):
            return re.match(r"(^[0-9]*$)", context) != None
        
        return False
    
    @staticmethod
    def is_boolean(context: str) -> bool:
        if isinstance(context, str):
            return context.lower() in ['true', 'false', '1', '0']

        if isinstance(context, bool):
            return True
        
        return False


    