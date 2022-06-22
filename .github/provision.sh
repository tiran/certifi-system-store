#!/bin/sh
set -ex

. /etc/os-release

if [ -e /usr/bin/dnf ]; then
    dnf update -y
    dnf install -y python3
    dnf clean all
elif [ -e /usr/bin/yum ]; then
    yum update -y
    yum install -y python3
    yum clean all
elif [ -e /usr/bin/apt ]; then
    apt update
    apt upgrade -y
    apt install -y python3 python3-venv ca-certificates
    apt clean
elif [ -e /sbin/apk ]; then
    apk add python3
    apk add python3-dev gcc musl-dev
elif [ -e /usr/bin/zypper ]; then
    zypper update -y
    zypper install -y python3
    zypper clean
else
    echo "Distro not supported"
    exit 1
fi
