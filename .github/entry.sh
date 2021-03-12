#!/bin/sh
set -ex

cd /tmp
python3 -m tox \
    --skip-missing-interpreters \
    -c /workdir/tox.ini \
    --workdir /tmp/tox
