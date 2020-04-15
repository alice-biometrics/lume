def check_list_or_str_item(kdict, key, required=False):
    kvalue = kdict.get(key)
    if not kvalue and required:
        raise TypeError(f"StepConfig must contains {key} variable")

    if isinstance(kvalue, str):
        value = [kvalue]
    elif isinstance(kvalue, list):
        value = kvalue
    else:
        if required:
            raise TypeError(
                f"StepConfig must contains {key} variable (Only list and str is supported)"
            )
        else:
            value = None
    return value
