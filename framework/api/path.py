import re


def capture_params(path: str, path_spec: str) -> dict:
    routes = []
    param_keys = []
    for route in path_spec.split('/'):
        match = re.search(r'^{(\w+)}$', route)
        if match:
            key = match.group(1)
            param_keys.append(key)
            routes.append(f'(?P<{key}>[\\w\\d]+)')
        else:
            routes.append(route)

    match = re.search('/'.join(routes), path)
    return {key: match.group(key) for key in param_keys}
