from datetime import tzinfo, timedelta


class TZInfo(tzinfo):
    def __init__(self, hours: int, dst: int, tzname: str) -> None:
        super(TZInfo, self).__init__()
        self._hours = hours
        self._dst = dst
        self._tzname = tzname

    def utcoffset(self, _) -> timedelta:
        return timedelta(hours=self._hours)

    def dst(self, _) -> timedelta:
        return timedelta(self._dst)

    def tzname(self, _) -> str:
        return self._tzname
