def routes() -> dict:
    return {
        'GET /users': 'example.webapi.api.users.index',
        'GET /users/{user_id}': 'example.webapi.api.users.show',
        'POST /users': 'example.webapi.api.users.create',
    }
