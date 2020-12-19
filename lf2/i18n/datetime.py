from datetime import date, datetime, time, tzinfo
from typing import Optional


class DateTime:
    def __init__(self, tz: tzinfo) -> None:
        self._tz = tz

    @property
    def tz(self) -> tzinfo:
        return self._tz

    def now(self) -> datetime:
        return datetime.now(tz=self._tz)

    def strftime(self, fmt: str) -> str:
        return self.now().strftime(fmt)

    def strptime(self, date: str, format: str) -> datetime:
        return datetime.strptime(date, format).replace(tzinfo=self._tz)

    def fromtimestamp(self, timestamp: float, tz: Optional[tzinfo] = None) -> datetime:
        return datetime.fromtimestamp(timestamp, tz=(self._tz if tz is None else tz))

    def fromisoformat(self, date_string: str) -> datetime:
        return datetime.fromisoformat(date_string)

    def today(self) -> datetime:
        return self.now().today()

    def utcnow(self) -> datetime:
        return datetime.utcnow()

    def utcfromtimestamp(self, timestamp: float) -> datetime:
        return datetime.utcfromtimestamp(timestamp)

    def fromordinal(self, ordinal: int) -> datetime:
        return datetime.fromordinal(ordinal)

    def combine(self, date: date, time: time, tzinfo: Optional[tzinfo]) -> datetime:
        return datetime.combine(date, time, tzinfo)
