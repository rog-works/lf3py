from datetime import tzinfo, timedelta


class TZInfo(tzinfo):
    def __init__(self, locale: str) -> None:
        super(tzinfo, self).__init__()
        definition = self.DEFINITIONS[locale]
        self._hours = definition['hours']
        self._dst = definition['dst']
        self._tzname = definition['tzname']

    def utcoffset(self, _) -> timedelta:
        return timedelta(hours=self._hours)

    def dst(self, _) -> timedelta:
        return timedelta(self._dst)

    def tzname(self, _) -> str:
        return self._tzname

    DEFINITIONS = {
        'ja': {'hours': 9, 'dst': 0, 'tzname': 'Asia/Tokyo'},
    }
