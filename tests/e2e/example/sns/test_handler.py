import example.sns.preprocess  # noqa F401

from unittest import TestCase, mock

from lf3py.aws.symbols import IFireHose
from lf3py.test.helper import data_provider


class TestHandler(TestCase):
    ADD_MODULES = {
        'lf3py.aws.symbols.IFireHose': 'tests.e2e.example.sns.test_handler.MockFireHose',
    }

    @data_provider([
        (
            {
                'Records': [
                    {
                        'TopicArn': 'dev_ping_topic',
                        'Subject': 'ping',
                        'Message': '',
                        'MessageAttributes': {},
                    },
                ],
            },
            {
                'topic': 'dev_ping_topic',
                'subject': 'ping',
                'message': 'pong',
            },
        ),
    ])
    def test_ping(self, event: dict, expected: dict):
        with mock.patch('example.sns.modules.add_modules', return_value=self.ADD_MODULES):
            with mock.patch('tests.e2e.example.sns.test_handler.MockFireHose.put') as p:
                from example.sns.handler import handler

                handler(event, object())
                p.assert_called_with(expected)

    @data_provider([
        (
            {
                'Records': [
                    {
                        'TopicArn': 'notice_topic',
                        'Subject': 'hoge',
                        'Message': 'fuga',
                        'MessageAttributes': {
                            'piyo': {
                                'Type': 'String',
                                'Value': 'hoge.fuga.piyo',
                            }
                        },
                    },
                ],
            },
            {
                'topic': 'notice_topic',
                'subject': 'hoge',
                'message': 'fuga',
                'values': {'piyo': 'hoge.fuga.piyo'},
            },
        ),
    ])
    def test_notice(self, event: dict, expected: dict):
        with mock.patch('example.sns.modules.add_modules', return_value=self.ADD_MODULES):
            with mock.patch('tests.e2e.example.sns.test_handler.MockFireHose.put') as p:
                from example.sns.handler import handler

                handler(event, object())
                p.assert_called_with(expected)


class MockFireHose(IFireHose):
    def __init__(self, delivery_stream_name: str = '') -> None:
        pass

    def put(self, payload: dict):
        pass
