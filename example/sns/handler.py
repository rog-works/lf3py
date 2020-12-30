from lf3py.aws.sns.data import SNSMessage
from lf3py.task.data import Result, Ok

from example.sns.app import MyApp
from example.sns.notice_defs import NoticeRecord, PingRecord


def handler(event: dict, context: object) -> dict:
    app = MyApp.entry(event)

    def run() -> dict:
        return app.run().serialize()

    @app.route('(?P<topic>(dev|test)_ping_topic)', 'ping')
    def ping(topic: str) -> Result:
        record = PingRecord(topic=topic, subject='ping', message='pong')
        app.firehose.put(record.serialize())
        return Ok

    @app.route('notice_topic', '(?P<subject>([\\w]+))')
    def notice(subject: str, message: SNSMessage) -> Result:
        record = NoticeRecord(
            topic='notice_topic',
            subject=subject,
            message=message.message,
            values={key: attr['value'] for key, attr in message.attributes.items()},
        )
        app.firehose.put(record.serialize())
        return Ok

    return run()
