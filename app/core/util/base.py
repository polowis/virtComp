import uuid


def generate_unique_id():
    """This function generates an unique."""
    return str(uuid.uuid1()).replace("-", "")
