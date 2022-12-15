import typing
from dl_manifest import get_manifest

import json

def main():
    man = get_manifest()
    print("latest release: " + get_latest_release(man))
    print("latest snapshot: " + get_latest_snapshot(man))

def get_latest_release(manifest: typing.Any) -> str:
    latest = manifest['latest']['release']
    return latest

def get_latest_snapshot(manifest: typing.Any) -> str:
    latest = manifest['latest']['snapshot']
    return latest

if __name__ == '__main__':
    main()