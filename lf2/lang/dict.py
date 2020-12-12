from typing import Union

Node = Union[int, float, str, dict, list]


def pluck(node: Node, path: str) -> Node:
    if type(node) is dict and path:
        key, *remain = path.split('.')
        return pluck(node[key], '.'.join(remain))
    elif type(node) is list and path:
        key, *remain = path.split('.')
        index = int(key)
        return pluck(node[index], '.'.join(remain))
    else:
        return node
