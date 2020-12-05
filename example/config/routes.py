from typing import Dict, Tuple

Routes = Dict[str, Tuple[str, str]]


def routes() -> Routes:
    return {
        'GET /users': ('example.controllers.users', 'index'),
        r'GET /users/\d+': ('example.controllers.users', 'show'),
        'POST /users': ('example.controllers.users', 'create'),
    }
