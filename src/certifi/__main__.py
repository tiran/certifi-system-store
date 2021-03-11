import argparse

from certifi import contents, where
from certifi._patch import _patch_dist_info

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contents", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()


_patched = _patch_dist_info()
if args.verbose:
    if _patched:
        print("Patched certifi.dist-info -> certifi_system_store.dist-info")
    else:
        print("certifi.dist-info already patched")

if args.contents:
    print(contents())
else:
    print(where())
