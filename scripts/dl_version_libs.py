import typing
import requests

def get_lib(man: typing.Any, name: str) -> typing.Any:
    for lib in man['libraries']:
        if lib['name'] == name:
            return lib

def get_all_libs(man: typing.Any) -> list:
    libs = []
    for lib in man['libraries']:
        libs.append(lib)
    return libs

def dl_lib(url: str, dest_path: str, size: int) -> None:
    r = requests.get(url)
    with open(dest_path, 'wb') as f:
        f.write(r.content)

def dl_all_libs(libs: list) -> typing.Any:
    for lib in libs:
        if 'url' in lib:
            artifacts = lib['downloads']['artifacts']
            dl_lib(artifacts['url'], str(artifacts['path']).split("/")[len(str(artifacts['path']).split("/")) - 1], artifacts['size'])

