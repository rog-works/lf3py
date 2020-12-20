from lf3py.app.provider import app_provider
from lf3py.app.snsapp import SNSApp
from lf3py.task.data import Result

from example.sns.notice_defs import NoticeMessage, NoticeRecord, PingRecord
import example.sns.provider as provider

app = app_provider(SNSApp)
firehose = provider.firehose()


@app.entry
def handler(event: dict, context: object) -> dict:
    return app.run().serialize()


@app.route('(?P<topic>(dev|test)_ping_topic)', 'ping')
def ping(topic: str) -> Result:
    record = PingRecord(topic=topic, subject='ping', message='pong')
    firehose.put(record.serialize())
    return record


@app.route('notice_topic', '(?P<subject>([\\w]+))')
def notice(subject: str, message: NoticeMessage) -> Result:
    record = NoticeRecord(
        topic='notice_topic',
        subject=subject,
        message=message.text,
        attributes=message.attributes,
    )
    firehose.put(record.serialize())
    return record
