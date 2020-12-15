import re


class Validator(object):

    @staticmethod
    def is_email(email: str) -> bool:
        """Return true if valid email expression"""
        if isinstance(email, str):
            return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None
        return False

    @staticmethod
    def is_alpha(context: str) -> bool:
        if isinstance(context, str):
            return re.match(r"(^[a-zA-Z])*$", context) is not None
        return False

    @staticmethod
    def is_alphanumeric(context: str) -> bool:
        """return true if given context only contains alphanumeric"""
        if isinstance(context, str):
            return re.match(r"(^[a-zA-Z0-9]*$)", context) is not None
        return False
    
    @staticmethod
    def is_number(context):
        if isinstance(context, int):
            return True
        
        if isinstance(context, str):
            return re.match(r"(^[0-9]*$)", context) is not None
        
        return False
    
    @staticmethod
    def is_boolean(context: str) -> bool:
        if isinstance(context, str):
            return context.lower() in ['true', 'false', '1', '0']

        if isinstance(context, bool):
            return True
        
        return False
    
    @staticmethod
    def has_below(context, value):
        if isinstance(context, str) and isinstance(value, int):
            return len(context) < value
        
        if isinstance(context, int) and isinstance(value, int):
            return context < value
        
        return False
    
    @staticmethod
    def has_above(context, value):
        if isinstance(context, str) and isinstance(value, int):
            return len(context) > value
        
        if isinstance(context, int) and isinstance(value, int):
            return context > value
        
        return False


            


    