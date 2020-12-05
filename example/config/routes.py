from typing import Dict, Tuple

Routes = Dict[str, Tuple[str, str]]

routes: Routes = {
    'GET /users': ('example.controllers.users', 'index'),
    r'GET /users/\d+': ('example.controllers.users', 'show'),
    'POST /users': ('example.controllers.users', 'create'),
}
