from lf3py.aws.firehose import FireHose


def firehose() -> FireHose:
    return FireHose('sns-delivery-stream')
