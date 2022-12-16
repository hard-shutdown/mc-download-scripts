import os
import typing
import requests
from pathlib import Path
from multiprocessing.pool import ThreadPool

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
    try:
        Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)
    except:
        pass
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise Exception("Failed to download library")
    if len(r.content) != size:
        raise Exception("Downloaded library is not the correct size")
    with open(dest_path, 'wb') as f:
        f.write(r.content)
        if verbose:
            print("Downloaded " + dest_path)

def dl_all_libs(libs: list, prefix: str, verbose: bool) -> typing.Any:
    arglist = []
    if verbose:
        print("Downloading " + str(len(libs)) + " libraries")
    pool = ThreadPool(len(libs))
    for lib in libs:
        if 'artifact' in lib['downloads']:
            artifacts = lib['downloads']['artifact']
            arglist.append((artifacts['url'], prefix + '/' + artifacts['path'], artifacts['size'], verbose))
        elif 'classifiers' in lib['downloads']:
            classifiers = lib['downloads']['classifiers']
            for classifier in classifiers:
                arglist.append((classifiers[classifier]['url'], prefix + '/' + classifiers[classifier]['path'], classifiers[classifier]['size'], verbose))
    pool.starmap(dl_lib, arglist)