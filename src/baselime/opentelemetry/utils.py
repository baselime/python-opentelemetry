import collections.abc


def sanitize_dict(dictionary):
    """
    Sanitize a dictionary by removing all None values
    :param dictionary: The dictionary to sanitize
    :return: A sanitized dictionary
    """
    return {k: v for k, v in dictionary.items() if v is not None}

def flatten(dictionary, parent_key=False, separator='.'):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :return: A flattened dictionary
    """

    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.abc.MutableMapping):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)

def flat(dictionary, parent_key=False):
    if not dictionary:
        return { parent_key: 'empty'}
    sanitized = sanitize_dict(dictionary)
    flattened = flatten(sanitized, parent_key)
    return flattened

print(flat(None))