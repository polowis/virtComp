import re


class Trimmer(object):

    class ValidationError(Exception):
        def __init__(self, messsage="Validation Error"):
            super().__init__(messsage)

    def __init__(self, request_content):
        self.request_content = request_content

    def alphanumeric(self, context=None):
        context = context if context is not None else self.request_content

        if isinstance(context, str):
            if re.match(r"(^[a-zA-Z0-9]*$)", context) is not None:
                return self
        raise Trimmer.ValidationError("The request is not alphanumeric")
    
    def email(self, context=None):
        if isinstance(context, str):
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", context) is not None:
                return self
        raise Trimmer.ValidationError("The request is not a valid email address")
    
    def required(self, context=None):
        context = context if context is not None else self.request_content
        if context is not None:
            return self
        raise Trimmer.ValidationError("The request field is required")
    
    def default(self, default_value=None, context=None):
        context = context if context is not None else self.request_content
        if default_value is None:
            raise Trimmer.ValidationError()
        if context is None:
            self.request_content = default_value
            return self
        raise Trimmer.ValidationError()
        
    def string(self, context=None):
        context = context if context is not None else self.request_content
        if isinstance(context, str):
            return self
        raise Trimmer.ValidationError()
