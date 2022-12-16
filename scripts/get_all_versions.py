import sys
from dl_manifest import get_manifest

def main():
    showall = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            showall = True
    man = get_manifest()
    for version in man['versions']:
        if version['type'] == 'release' or showall:
            print(version['id'])

if __name__ == '__main__':
    main()