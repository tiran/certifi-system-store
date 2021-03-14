import os
import ssl

import certifi
import pkg_resources


def test_where():
    assert os.path.isfile(certifi.where())


def test_contents():
    contents = certifi.contents()
    assert "BEGIN CERTIFICATE" in contents


def test_is_css():
    assert certifi.__certifi_system_store__


def test_version():
    for distname in ("certifi", "certifi_system_store"):
        dist = pkg_resources.get_distribution(distname)
        assert dist.version.startswith("30")


def test_ssl_load_certs():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    assert not ctx.get_ca_certs()
    ctx.load_verify_locations(cafile=certifi.where())
    cacerts = ctx.get_ca_certs()
    assert len(cacerts)
