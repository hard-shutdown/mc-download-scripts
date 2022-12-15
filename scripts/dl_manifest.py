import typing
import requests
import json

# Get the manifest
def main():
    # Save the manifest
    with open('version_manifest.json', 'wb') as f:
        f.write(json.dumps(get_manifest(), indent=4).encode('utf-8'))

def get_manifest() -> typing.Any:
    r = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    return json.loads(r.text)

def save_manifest(manifest: typing.Any) -> None:
    with open('version_manifest.json', 'wb') as f:
        f.write(json.dumps(manifest, indent=4).encode('utf-8'))

if __name__ == '__main__':
    main()