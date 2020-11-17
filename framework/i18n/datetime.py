from datetime import datetime, tzinfo


class DateTime:
    def __init__(self, tz: tzinfo) -> None:
        self._tz = tz

    def now(self) -> datetime:
        return datetime(tzinfo=self._tz).now

    def strftime(self, fmt: str) -> datetime:
        return datetime(tzinfo=self._tz).strftime(fmt)

    def strptime(self, date: str, format: str) -> datetime:
        return datetime.strptime(date, format).replace(tzinfo=self._tz)
