import typing
from dl_manifest import get_manifest

import requests
import json
import sys

def main():
    versions_manifest = get_manifest()
    with open(sys.argv[1].replace(".", "-") + '_manifest.json', 'wb') as f:
        f.write(json.dumps(get_manifest_for_version(versions_manifest, sys.argv[1]), indent=4, sort_keys=True).encode('utf-8'))

def get_manifest_for_version(man: typing.Any, wanted_version: str) -> typing.Any:
    for version in man['versions']:
        if version['id'] == wanted_version:
            r = requests.get(version['url'], timeout=10)
            if r.status_code != 200:
                raise Exception("Failed to get version manifest")
            return r.json()
    raise Exception("Version not found")

if __name__ == '__main__':
    main()
