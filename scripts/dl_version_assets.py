import os
import typing
import requests
import json
from pathlib import Path
from multiprocessing.pool import ThreadPool

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_asset_by_name(man: typing.Any, name: str) -> typing.Any:
    if name in man["objects"]:
        return man["objects"][name]
    
def get_asset_by_hash(man: typing.Any, hash: str) -> typing.Any:
    for obj in man['objects']:
        if man['objects'][obj]['hash'] == hash:
            return json.loads('{"hash":"' + man['objects'][obj]['hash'] + '","size":' + str(man['objects'][obj]['size']) + ',"name":"' + obj + '"}')

def get_all_assets(man: typing.Any) -> list:
    objs = []
    for obj in man['objects']:
        objs.append(man['objects'][obj])
    return objs

def get_url_for_asset(hash: str) -> str:
    return "https://resources.download.minecraft.net/" + hash[:2] + "/" + hash

def dl_asset(url: str, dest_path: str, size: int, verbose: bool) -> None:
    try:
        Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    r = requests.get(url, timeout=10, stream=True)
    if r.status_code != 200:
        raise Exception("Failed to download library")
    if len(r.content) != size:
        raise Exception("Downloaded library is not the correct size")
    with open(dest_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192): 
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            #if chunk: 
            f.write(chunk)
        if verbose:
            print("Downloaded " + dest_path)

def dl_all_assets(objects: list, prefix: str, verbose: bool) -> typing.Any:
    arglist = []
    if verbose:
        print("Downloading " + str(len(objects)) + " assets")
    pool = ThreadPool(len(objects))
    for obj in objects:
        arglist.append((get_url_for_asset(obj["hash"]), prefix + '/' + obj['hash'][:2] + "/" + obj['hash'], obj['size'], verbose))
    chunked = list(divide_chunks(arglist, 50))
    for chunk in chunked:
        pool.starmap(dl_asset, chunk)
