from datetime import datetime, tzinfo


class DateTime:
    def __init__(self, tz: tzinfo) -> None:
        self._tz = tz

    def now(self) -> datetime:
        return datetime.now(tz=self._tz)

    def strftime(self, fmt: str) -> str:
        return self.now().strftime(fmt)

    def strptime(self, date: str, format: str) -> datetime:
        return datetime.strptime(date, format).replace(tzinfo=self._tz)
