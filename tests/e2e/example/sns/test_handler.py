import example.sns.preprocess  # noqa F401

from unittest import TestCase, mock

from lf3py.test.helper import data_provider

from tests.helper.example.sns import perform_api


class TestHandler(TestCase):
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
        with mock.patch('boto3.client', return_value=object()):
            with mock.patch('lf3py.aws.firehose.FireHose.put') as p:
                perform_api(event)
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
        with mock.patch('boto3.client', return_value=object()):
            with mock.patch('lf3py.aws.firehose.FireHose.put') as p:
                perform_api(event)
                p.assert_called_with(expected)
