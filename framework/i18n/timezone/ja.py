from datetime import tzinfo, timedelta


class JA(tzinfo):
    def utcoffset(self, _) -> timedelta:
        return timedelta(hours=9)

    def dst(self, _) -> timedelta:
        return timedelta(0)

    def tzname(self, _) -> str:
        return 'Asia/Tokyo'
