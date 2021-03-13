import argparse

from certifi import contents, where, __version__
from certifi._patch import _patch_dist_info


parser = argparse.ArgumentParser(prog="certifi-system-store")
parser.add_argument("-c", "--contents", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--system-store", action="store_true")
args = parser.parse_args()


_patched = _patch_dist_info()
if args.verbose:
    print(f"certifi-system store {__version__}")
    if _patched:
        print("Patched certifi.dist-info -> certifi_system_store.dist-info")
    else:
        print("certifi.dist-info already patched")

if args.contents:
    print(contents())
else:
    print(where())
