from dl_manifest import get_manifest
from dl_version_manifest import get_manifest_for_version
from dl_version_libs import get_all_libs, dl_all_libs
from download_jar import download_jar

import sys
import os

def main():
    man = get_manifest()
    version_manifest = get_manifest_for_version(man, sys.argv[1])
    libs = get_all_libs(version_manifest)
    os.chdir((os.getenv("TEMP") if os.name=="nt" else "/tmp"))
    dl_all_libs(libs)
    download_jar(version_manifest, sys.argv[1].replace(".", "-") + "client.jar", sys.argv[1], "client")