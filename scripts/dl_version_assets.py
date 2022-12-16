import os
import typing
import requests
from pathlib import Path
from multiprocessing.pool import ThreadPool

def get_asset_by_name(man: typing.Any, name: str) -> typing.Any:
    if name in man["objects"]:
        return man["objects"][name]
    
def get_asset_by_hash(man: typing.Any, hash: str) -> typing.Any:
    for obj in man['objects']:
        if obj['hash'] == hash:
            return obj

def get_all_assets(man: typing.Any) -> list:
    objs = []
    for obj in man['objects']:
        objs.append(obj)
    return objs

def get_url_for_asset(hash: str) -> str:
    return "https://resources.download.minecraft.net/" + hash[:2] + "/" + hash

def dl_asset(url: str, dest_path: str, size: int, verbose: bool) -> None:
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

def dl_all_assets(objects: list, prefix: str, verbose: bool) -> typing.Any:
    arglist = []
    if verbose:
        print("Downloading " + str(len(objects)) + " libraries")
    pool = ThreadPool(len(objects))
    for obj in objects:
        arglist.append((get_url_for_asset(obj["hash"]), prefix + '/' + hash[:2] + "/" + hash, obj['size'], verbose))
    pool.starmap(dl_asset, arglist)
