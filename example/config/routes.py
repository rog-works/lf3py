def routes() -> dict:
    return {
        'GET /users': 'example.controllers.users.index',
        'GET /users/{user_id}': 'example.controllers.users.show',
        'POST /users': 'example.controllers.users.create',
    }
