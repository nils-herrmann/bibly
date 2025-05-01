def get_field_value(dictionary: dict, field: str, default=None):
    """
    Get the value of a field from a dictionary. If the field does not exist OR is None, return the default value.
    """
    item = dictionary.get(field)
    if item is None:
        return default
    else:
        return item