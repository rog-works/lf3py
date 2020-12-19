import uuid


def make_context() -> dict:
    return {
        'correlation_id': str(uuid.uuid4()),
    }
