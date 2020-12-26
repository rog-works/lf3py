def modules() -> dict:
    return {
        'lf3py.routing.routers.Router': 'lf3py.routing.routers.flow.FlowRouter',
        'lf3py.symbols.IFireHose': 'example.sns.provider.firehose',
        'lf3py.aws.sns.record.SNSRecords': 'lf3py.aws.sns.provider.records',
    }
