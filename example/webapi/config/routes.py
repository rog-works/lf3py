def routes() -> dict:
    return {
        'GET /users': 'example.webapi.controllers.users.index',
        'GET /users/{user_id}': 'example.webapi.controllers.users.show',
        'POST /users': 'example.webapi.controllers.users.create',
    }
