import json
import typing
import requests

def main():
    with open('version_manifest.json', 'wb') as f:
        f.write(json.dumps(get_manifest(), indent=4).encode('utf-8'))

def get_manifest() -> typing.Any:
    r = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json', timeout=10)
    if r.status_code != 200:
        raise Exception("Failed to get manifest")
    return json.loads(r.text)

def save_manifest(manifest: typing.Any) -> None:
    with open('version_manifest.json', 'wb') as f:
        f.write(json.dumps(manifest, indent=4).encode('utf-8'))

if __name__ == '__main__':
    main()