#!/bin/sh
set -ex

if [ -f /etc/os-release ]; then
    . /etc/os-release
fi

# check that default setuptools can handle setup.cfg and setup.py
python3 -m pip list
if [ "$VERSION_ID" != "18.04" ]; then
    # setuptools on Ubuntu Bionic doesn't like attr: with src/
    python3 setup.py egg_info sdist
fi

# update to latest setuptools, pipm and tox
python3 -m pip install --upgrade pip setuptools tox
python3 -m tox -e py3-test,py3-requests
