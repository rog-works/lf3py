Lambda Function Framewark for Python (lf3py)
===

[![CircleCI](https://circleci.com/gh/rog-works/lambda-fw.svg?style=shield)](https://circleci.com/gh/rog-works/lambda-fw)
[![Coverage Status](https://coveralls.io/repos/github/rog-works/lambda-fw/badge.svg?branch=master)](https://coveralls.io/github/rog-works/lambda-fw?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/57516db91d69b07a76b5/maintainability)](https://codeclimate.com/github/rog-works/lambda-fw/maintainability)

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
from lf3py.app.provider import app_provider
from lf3py.app.webapp import WebApp

app = app_provider(WebApp, WebApp.default_modeules())


@app.entry
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@app.route('GET', '/ping')
def pong() -> Response:
    return app.render.ok().json()


# XXX cui testing code
if __name__ == '__main__':
    event = {
        'httpMethod': '/GET',
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
