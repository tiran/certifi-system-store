#!/bin/sh
set -ex

. /etc/os-release

if [ -e /usr/bin/dnf ]; then
    dnf update -y
    dnf install -y python3-pip
    dnf clean all
elif [ -e /usr/bin/yum ]; then
    yum update -y
    yum install -y python3 python3-pip
    yum clean all
elif [ -e /usr/bin/apt ]; then
    apt update
    apt upgrade -y
    apt install -y python3 python3-pip ca-certificates
    apt clean
elif [ -e /sbin/apk ]; then
    apk add python3 py3-pip
    apk add python3-dev gcc musl-dev
elif [ -e /usr/bin/zypper ]; then
    zypper update -y
    zypper install -y python3-pip
    zypper clean
else
    echo "Distro not supported"
    exit 1
fi
