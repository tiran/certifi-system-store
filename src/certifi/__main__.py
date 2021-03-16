import argparse

from certifi import contents, where, __version__
from certifi._patch import _patch_dist_info


parser = argparse.ArgumentParser(prog="certifi-system-store")
parser.add_argument("-c", "--contents", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--system-store", action="store_true")
args = parser.parse_args()

try:
    _patched, _css_dist_info, _certifi_dist_info = _patch_dist_info()
except OSError as e:
    parser.exit(3, f"Failed to patch certifi's dist-info: {e}\n")

if args.verbose:
    print(f"certifi-system store {__version__}")
    if _patched:
        print("Successfully patched certifi's dist-info")
    else:
        print("certifi.dist-info already patched")
    print(f"{_certifi_dist_info} -> {_css_dist_info}")

if args.contents:
    print(contents())
else:
    print(where())
