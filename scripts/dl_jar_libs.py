import random
import shutil
import zipfile
import sys
import os

import requests

from pathlib import Path

from dl_manifest import get_manifest
from dl_version_manifest import get_manifest_for_version
from dl_version_libs import get_all_libs, dl_all_libs
from dl_version_assets import dl_all_assets, get_all_assets
from download_jar import download_jar

def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(source_dir)
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_BZIP2) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)


def main():
    actualdir = os.getcwd()
    man = get_manifest()
    version_manifest = get_manifest_for_version(man, sys.argv[1])
    libs = get_all_libs(version_manifest)
    rand = str(random.uniform(1, 100000))
    tmpdir = (os.getenv("TEMP") if os.name=="nt" else "/tmp") + "/mc-dl--/" + rand
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    os.chdir(tmpdir)
    with open(sys.argv[1] + "_manifest.json", "w", encoding='utf8') as f:
        f.write(str(version_manifest))
    dl_all_libs(libs, 'libraries', True)
    dl_all_assets(get_all_assets(requests.get(version_manifest["assetIndex"]["url"], timeout=10).json()), 'assets/objects', True)
    print("Downloading " + sys.argv[1] + " client jar")
    download_jar(man, sys.argv[1] + "_client.jar", sys.argv[1], "client")
    print("Compressing")
    make_zipfile(actualdir + "/" + sys.argv[1] + "_bundle.zip", '.')
    os.chdir(actualdir)
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()