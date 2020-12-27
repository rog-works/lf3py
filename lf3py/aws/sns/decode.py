from lf3py.aws.types import LambdaEvent
from lf3py.aws.sns.record import SNSRecord, SNSRecords
from lf3py.lang.sequence import last


def decode_records(event: LambdaEvent) -> SNSRecords:
    return [
        SNSRecord(
            record={
                'topic': last(record['TopicArn'].split(':')),
                'subject': record['Subject'],
                'message': record['Message'],
                'attributes': {
                    key: {'type': attr['Type'], 'value': attr['Value']}
                    for key, attr in record['MessageAttributes'].items()
                },
            }
        ) for record in event['Records']
    ]
