from datetime import datetime, tzinfo
import json
import logging
from typing import List


class JsonFormatter(logging.Formatter):
    def __init__(self, keys: List[str], date_format: str = '%Y-%m-%dT%H:%M:%S.%f%z', tz: tzinfo = tzinfo()) -> None:
        super(JsonFormatter, self).__init__()
        self._keys = keys
        self._date_format = date_format
        self._tz = tz

    def format(self, record: logging.LogRecord) -> str:
        data = {key: str(getattr(record, key)) for key in self._keys if hasattr(record, key)}

        if 'created' in data:
            timestamp = float(data['created'])
            data['created'] = datetime.fromtimestamp(timestamp, tz=self._tz).strftime(self._date_format)

        return json.dumps(data)
