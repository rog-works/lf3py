import json
import sys

from bin.discovery import Discovery, OpenApiGenerator


if __name__ == '__main__':
    _, *filepaths = sys.argv
    discovery = Discovery(list(filepaths))
    print(json.dumps(discovery.generate(OpenApiGenerator()), indent=4))
