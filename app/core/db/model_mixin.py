from typing import Any


def get_modified_fields(old_values, new_values):
    """
    Return all fields that have been modified from original fields
    """
    field_changes = {}

    for key, value in new_values.items():
        try:

            original_value = old_values[key]
        except KeyError:
            """If there are addtional attributes which are not present in the database"""
            continue

        if original_value != value:
            field_changes[key] = {'original': original_value, 'modified': value}
    
    return field_changes


class ModelMixin(object):
    def __init__(self):
        self.original_states = self.get_original_states()
    
    def get_original_states(self) -> dict:
        """
        Get the original model attributes
        """
        old_values = self.get_fields_details_as_dict()
        return old_values
    
    def get_fields_details_as_dict(self) -> dict:
        """
        Return the key value pair denotes the current model attributes in META field as dict.
        """
        values = {}
        for field in self._meta.fields:
            field_names = field.get_attname()
            field_value = getattr(self, field.attname)
            values[field_names] = field_value
        return values

    def get_dirty_fields(self) -> dict:
        """
        Return the dictionary of modified fields since the model was retrieved
        """
        modified_fields = get_modified_fields(
            old_values=self.original_states,
            new_values=self.get_fields_details_as_dict())
        return modified_fields
    
    def is_dirty(self, key_to_check=None) -> bool:
        """
        The is_dirty method determines if any of the model's attributes have been
        changed since the model was retrieved.

        You may pass a specific attribute name to the is_dirty method to determine
        if a particular attribute is dirty.
        """
        if key_to_check:
            try:
                self.get_dirty_fields()[key_to_check]
                return True
            except KeyError:
                """If key is not presented in the dirty fields means the key is not dirty"""
                return False
        return {} != self.get_dirty_fields()
    
    def is_clean(self, key_to_check=None) -> bool:
        """
        The is_clean method determines if any of the model's attributes have been
        unchanged since the model was retrieved.
        
        You may pass a specific attribute name to the is_clean method to determine
        if a particular attribute is clean.
        """
        return not self.is_dirty(key_to_check)
    
    def get_original(self, key_to_lookup: str = None) -> Any:
        """
        Get the original value of the given key
        """
        if key_to_lookup is None:
            return self.original_states
        return self.original_states[key_to_lookup]
    
    def as_dict(self, *args) -> dict:
        """
        Return the model meta atrribute as dictionary.
        It will not return any attributes specified in protected field

        If any argument is provided, it will return only the one specified even if it
        is protected and will ignore the protected fields. You may also pass unprotected field in model
        as well. But keep in mind that unprotected fields will be prioritized as protected will be ignore
        to prevent clashing

        """
        attrs: dict = self.get_original_states()
        model_unprotected_field = getattr(self, 'unprotected', None)
        
        if len(args) > 0:  # if custom fields exists:
            values = {key: value for key, value in attrs.items() if key in args}
            return values

        # if model unprotected field exists
        if model_unprotected_field is not None:
            values = {key: value for key, value in attrs.items() if key in model_unprotected_field}
            return values

        # if protected field exists
        protected_values: list = getattr(self, 'protected', None)
        if protected_values is None:
            return attrs
        else:
            for value in protected_values:
                try:
                    del attrs[value]
                except KeyError:
                    continue
            
            return attrs
