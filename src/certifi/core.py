import os

from certifi._patch import _verify_dist_info

_CANDIDATES = [
    # Alpine, Arch, Fedora 34+, OpenWRT, RHEL 9+, ...
    "/etc/ssl/cert.pem",
    # Fedora <= 34, RHEL <= 9, CentOS <= 9
    "/etc/pki/tls/cert.pem",
    # Debian, Ubuntu (requires ca-certificates)
    "/etc/ssl/certs/ca-certificates.crt",
    # SUSE
    "/etc/ssl/ca-bundle.pem",
]
_SSL_PEM = None


def read_text(_module, _path, encoding="utf-8"):
    with open(where(), "r", encoding=encoding) as data:
        return data.read()


def where():
    global _SSL_PEM
    if _SSL_PEM is not None:
        return _SSL_PEM
    _verify_dist_info()
    for candidate in _CANDIDATES:
        if os.path.isfile(candidate):
            _SSL_PEM = candidate
            return _SSL_PEM
    else:
        raise FileNotFoundError(", ".join(_CANDIDATES))


def contents():
    return read_text("certifi", "cacert.pem", encoding="utf-8")
