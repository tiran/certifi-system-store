#!/bin/sh
set -ex

# run in venv to work around Debian/Ubuntu downstream patches
# --upgrade-deps is not available in older distros
python3 -m venv testenv
testenv/bin/python3 -m pip install --upgrade pip setuptools
testenv/bin/python3 -m pip install tox
testenv/bin/python3 -m tox -e py3-test,py3-requests
