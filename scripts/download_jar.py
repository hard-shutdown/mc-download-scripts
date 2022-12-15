from dl_version_manifest import get_manifest_for_version
from dl_manifest import get_manifest

import typing
import requests
import json
import sys

def main():
    versions_manifest = get_manifest()
    download_jar(versions_manifest, sys.argv[1].replace(".", "-") + '_client.jar', sys.argv[1], 'client')
    print(sys.argv[1].replace(".", "-") + '_client.jar', end='')

def download_jar(man: typing.Any, dest_path: str, version: str, type: str):
    version_manifest = get_manifest_for_version(man, version)
    with open(dest_path, 'wb') as f:
        r = requests.get(version_manifest['downloads'][type]['url'], timeout=10)
        if r.status_code != 200:
            raise Exception("Failed to download " + type)
        if len(r.content) != version_manifest['downloads'][type]['size']:
            raise Exception("Downloaded" + type + "is not the correct size")
        f.write(r.content)

if __name__ == '__main__':
    main()