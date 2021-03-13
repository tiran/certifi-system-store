# certifi-system-store, a certifi hack

*certifi-system-store* is a replacement and hack for consumers of
*certifi*. It replaces certifi with an alternative implementation that
uses the system trust store on Linux and some BSD distributions.

## Installation

You absolutely **must** run ``python -m certifi`` after installing the
package. The command ensures that you have a working system trust store
and patches your current Python environment. It creates or replaces
certifi's dist-info directory with certifi-system-store's dist-info.

```
$ python -m pip install certifi-system-store
$ python -m certifi
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
* OpenWRT

### Untested platforms

* ArchLinux
* Gentoo
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

## How does it work?

* empty ``certifi/cacert.pem`` to override any existing certifi data.
* fake ``certifi dist-info`` with much higher version number than certifi's
  default dist-info metadata

```
$ venv/bin/pip install certifi-system-store
$ ls -l .tox/venv/lib/python3.9/site-packages/
certifi
certifi_system_store-3000.1.dist-info
...
$ venv/bin/python -m certifi -v
Patched certifi.dist-info -> certifi_system_store.dist-info
/etc/pki/tls/cert.pem
$ ls -l .tox/venv/lib/python3.9/site-packages/
certifi
certifi-3000.1.dist-info -> certifi_system_store-3000.1.dist-info
certifi_system_store-3000.1.dist-info
...
```
