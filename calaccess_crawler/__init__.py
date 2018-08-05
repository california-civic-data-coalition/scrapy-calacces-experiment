import inspect
from . import items


def get_items():
    """
    Returns a list of all the item classes in this project.
    """
    # Inspect the module to get all the classes as a dict, with the names as keys.
    inspect_dict = dict(inspect.getmembers(items, inspect.isclass))
    # Return the classes as a list
    return list(inspect_dict.values())
