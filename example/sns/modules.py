def modules() -> dict:
    return {
        'lf3py.aws.sns.record.SNSRecords': 'lf3py.aws.sns.decode.decode_records',
        'lf3py.aws.symbols.IFireHose': 'example.sns.provider.firehose',
        'lf3py.routing.symbols.IRouter': 'lf3py.routing.router.FlowRouter',
    }
