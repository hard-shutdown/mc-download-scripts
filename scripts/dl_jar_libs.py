import random
import shutil
import zipfile
import sys
import os

from dl_manifest import get_manifest
from dl_version_manifest import get_manifest_for_version
from dl_version_libs import get_all_libs, dl_all_libs
from download_jar import download_jar

def main():
    actualdir = os.getcwd()
    man = get_manifest()
    version_manifest = get_manifest_for_version(man, sys.argv[1])
    libs = get_all_libs(version_manifest)
    tmpdir = (os.getenv("TEMP") if os.name=="nt" else "/tmp") + "/" + str(random.uniform(1, 100000))
    os.mkdir(tmpdir)
    os.chdir(tmpdir)
    dl_all_libs(libs, True)
    print("Downloading " + sys.argv[1] + " client jar")
    download_jar(man, sys.argv[1].replace(".", "-") + "_client.jar", sys.argv[1], "client")
    with zipfile.ZipFile(actualdir + "/" + sys.argv[1].replace(".", "-") + "_client.zip", "w") as zip:
        for file in os.listdir(tmpdir):
            zip.write(file)
    os.chdir(actualdir)
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()