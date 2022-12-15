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

def dl_lib(url: str, dest_path: str, size: int, verbose: bool) -> None:
    if verbose:
        print("Downloading " + dest_path)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise Exception("Failed to download library")
    if len(r.content) != size:
        raise Exception("Downloaded library is not the correct size")
    with open(dest_path, 'wb') as f:
        f.write(r.content)

def dl_all_libs(libs: list, verbose: bool) -> typing.Any:
    for lib in libs:
        if 'artifact' in lib['downloads']:
            artifacts = lib['downloads']['artifact']
            dl_lib(artifacts['url'], str(artifacts['path']).split("/")[len(str(artifacts['path']).split("/")) - 1], artifacts['size'], verbose)
        elif 'classifiers' in lib['downloads']:
            classifiers = lib['downloads']['classifiers']
            for classifier in classifiers:
                dl_lib(classifiers[classifier]['url'], str(classifiers[classifier]['path']).split("/")[len(str(classifiers[classifier]['path']).split("/")) - 1], classifiers[classifier]['size'], verbose)
