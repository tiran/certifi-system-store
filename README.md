# certifi-system-store, a certifi hack to use system trust store

*certifi-system-store* is a replacement and hack for consumers of
*certifi*. It replaces certifi with an alternative implementation that
uses the system trust store on Linux and some BSD distributions.

Please be advised that this package is brand new and **highly
experimental**. It hasn't been tested in any production environment.

## Installation

You absolutely **must** run ``python -m certifi`` after installing the
package. The command ensures that you have a working system trust store
and patches your current Python environment. It creates or replaces
certifi's dist-info directory with certifi-system-store's dist-info.

I recommend that you install ``certifi-system-store`` and patch first,
then install your packages and requirements.

```shell
$ python -m pip install certifi-system-store
$ python -m certifi
$ python -m pip install requests
```

### Verification

The ``certifi`` command of ``certifi-system-store`` has an additional
argument ``--system-store``. The argument is not available with standard
``certifi`` package. You can use the property to verify that ``certifi``
package is provided by ``certifi-system-store``.

```shell
$ python -m venv venv
$ venv/bin/pip install certifi
$ venv/bin/python -m certifi --system-store
usage: __main__.py [-h] [-c]
__main__.py: error: unrecognized arguments: --system-store
$ echo $?
2
```

```shell
$ venv/bin/pip install certifi-system-store
$ venv/bin/python -m certifi --system-store
/etc/pki/tls/cert.pem
$ echo $?
0
```

The command also checks for the presence of a CA cert bundle:

```shell
$ venv/bin/python -m certifi
Traceback (most recent call last):
  ...
FileNotFoundError: /etc/ssl/cert.pem, /etc/pki/tls/cert.pem, /etc/ssl/certs/ca-certificates.crt, /etc/ssl/ca-bundle.pem
$ echo $?
1
```

To check for ``certifi-system-store`` at runtime:

```python
import certifi

if not getattr(certifi, "__certifi_system_store__", False):
    raise ImportError("certifi-system-store is not installed")
```

To depend on ``certifi-system-store``:

```python
# setup.py
from setuptools import setup

setup(
    ...,
    install_requires=[
        "certifi-system-store ; sys_platform == 'linux' or 'freebsd' in sys_platform",
        "certifi > 3000 ; sys_platform == 'linux' or 'freebsd' in sys_platform",
        "certifi",
    ],
)
```

## Platform support

### Supported platforms

Most major Linux distributions and FreeBSD are supported.

* Alpine
* Debian-based distributions (Ubuntu, Raspberry Pi OS, Tails, ...)
  * **NOTE:** Some distributions don't have a system trust store in
    their minimal package list. You may have to install
    ``ca-certificates`` manually, see
    [Debian bug #960869](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=960869),
    [Ubuntu bug #1879310](https://bugs.launchpad.net/ubuntu/+source/python3.6/+bug/1879310).
* Fedora-based distributions (RHEL, CentOS, CentOS Streams)
* FreeBSD
  * **NOTE:** may require manual installation of ``ca_root_nss``
* OpenSUSE

### Untested platforms

``certifi-system-store`` may work, but there is no CI for these platforms.

* ArchLinux
* Gentoo
* OpenWRT
* Slackware
* VoidLinux
* other Linux distributions not based on Debian or Fedora
* OpenBSD
* NetBSD

### Unsupported platforms

* Windows
* macOS
* Android (has a cert directory but not a PEM bundle)
* iOS

## Supported system trust stores

### ``/etc/ssl/cert.pem``

* Alpine
* Arch
* Fedora 34+ (see [rhbz#1895619](https://bugzilla.redhat.com/show_bug.cgi?id=1895619))
* FreeBSD (requires ``ca_root_nss`` package)
* OpenWRT
* RHEL 9

### ``/etc/pki/tls/cert.pem``

* CentOS 7, 8
* Fedora 33 and earlier
* RHEL 7, 8

### ``/etc/ssl/certs/ca-certificates.crt``

* Debian (requires ``ca-certificates`` package)
* Gentoo
* Ubuntu (requires ``ca-certificates`` package)

### ``/etc/ssl/ca-bundle.pem``

* SUSE


## How to install custom CA certificates

### Alpine

```shell
$ sudo cp my-custom-ca.pem /usr/local/share/ca-certificates/my-custom-ca.crt
$ sudo update-ca-certificates
```

### Arch

```shell
$ sudo cp my-custom-ca.pem /etc/ca-certificates/trust-source/anchors/my-custom-ca.crt
$ sudo update-ca-trust
```

### CentOS, Fedora, RHEL

Standard PEM or DER-encoded certificates (``BEGIN CERTIFICATE``)

```shell
$ sudo cp my-custom-ca.pem /etc/pki/ca-trust/source/anchors/
$ sudo update-ca-trust
```

Certificates with additional trust information
(``BEGIN TRUSTED CERTIFICATE``)

```shell
$ sudo cp my-custom-ca.pem /etc/pki/ca-trust/source/
$ sudo update-ca-trust
```

### Debian, Ubuntu

Note: The man page ``update-ca-certificates(8)`` mentions that cert
files must have a ``.crt`` extension.

```shell
$ sudo cp my-custom-ca.pem /usr/local/share/ca-certificates/my-custom-ca.crt
$ sudo update-ca-certificates
```


## How does it work?

* empty ``certifi/cacert.pem`` to override any existing certifi data.
* fake ``certifi dist-info`` with much higher version number than certifi's
  default dist-info metadata

```shell
$ venv/bin/pip install certifi-system-store
$ ls -l .tox/venv/lib/python3.9/site-packages/
certifi
certifi_system_store-3000.1.dist-info
...
$ venv/bin/python -m certifi -v --system-store
certifi-system store 3000.0a1
Patched certifi.dist-info -> certifi_system_store.dist-info
/etc/pki/tls/cert.pem
$ ls -l .tox/venv/lib/python3.9/site-packages/
certifi
certifi-3000.1.dist-info -> certifi_system_store-3000.1.dist-info
certifi_system_store-3000.1.dist-info
...
```

## Special thanks

* Cory Benfield
* Pradyun Gedam
* Wouter Bolsterlee
