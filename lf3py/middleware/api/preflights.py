from lf3py.api.cors import CorsSetting
from lf3py.api.response import Response


def cors(response: Response, cors: CorsSetting):
    cors_headers = {
        'Access-Control-Allow-Origin': cors.allow_origin,
        'Access-Control-Allow-Methods': ', '.join(cors.allow_methods),
        'Access-Control-Allow-Headers': ', '.join(cors.allow_headers),
        'Access-Control-Max-Age': cors.max_age,
    }
    response.headers = {**response.headers, **cors_headers}
