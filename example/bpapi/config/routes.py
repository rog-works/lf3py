def routes() -> dict:
    return {
        'GET /users': 'example.bpapi.api.users.index',
        'GET /users/{user_id}': 'example.bpapi.api.users.show',
        'POST /users': 'example.bpapi.api.users.create',
    }
