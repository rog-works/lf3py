Lambda Function Framewark for Python (lf3py)
===

[![CircleCI](https://circleci.com/gh/rog-works/lf3py.svg?style=shield)](https://circleci.com/gh/rog-works/lf3py)
[![Coverage Status](https://coveralls.io/repos/github/rog-works/lf3py/badge.svg?branch=master)](https://coveralls.io/github/rog-works/lf3py?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/57516db91d69b07a76b5/maintainability)](https://codeclimate.com/github/rog-works/lf3py/maintainability)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

# Requirements

* Python: >=3.7

# Usage

## Simple API backend

### Install package

```sh
$ pip install lf3py
```

### Create `lambda_handler.py`

```sh
$ vim lambda_handler.py
```

```python
from lf3py.api.response import Response
from lf3py.app.apiapp import ApiApp


def handler(event: dict, context: object) -> dict:
    app = ApiApp.entry(event)

    def run() -> dict:
        return app.run().serialize()

    @app.api.get('/ping')
    def pong() -> Response:
        return app.render.ok().json()

    return run()


# XXX cui testing code
if __name__ == '__main__':
    event = {
        'httpMethod': 'GET',
        'path': '/ping',
        'headers': {},
    }
    print(handler(event, object()))
```

### Testing `lambda_handler.py`

```sh
$ python lambda_handler.py | python -m json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {}
}
```
