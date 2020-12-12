import re
from typing import Dict

from lf2.lang.dsn import DSN, DSNElement


class PathDSN(DSN):
    @classmethod
    def format(cls, *elems: DSNElement) -> str:
        return ' '.join([str(elem) for elem in elems])

    def like(self, spec: str) -> bool:
        pattern = self._spec_to_pattern(spec)
        return re.search(pattern, self._dsn) is not None

    def capture(self, spec: str) -> Dict[str, str]:
        pattern = self._spec_to_pattern(spec)
        match = re.search(pattern, self._dsn)
        return match.groupdict() if match is not None else {}

    def _spec_to_pattern(self, spec: str) -> str:
        elems = []
        for elem in spec.split('/'):
            match = re.search(r'^{(\w+)}$', elem)
            if match:
                key = match.group(1)
                elems.append(f'(?P<{key}>[\\w\\d]+)')
            else:
                elems.append(elem)

        return f'^{"/".join(elems)}$'
