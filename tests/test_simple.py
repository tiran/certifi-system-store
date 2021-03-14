import os
import ssl
import sys

import pkg_resources
import pytest

import certifi


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


@pytest.mark.skipif(sys.platform.startswith("freebsd"), reason="Fails on FreeBSD 12.2")
def test_distrusted_ca_in_truststore():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(cafile=certifi.where())

    cns = set()
    for info in ctx.get_ca_certs():
        for dn in info["subject"]:
            for key, value in dn:
                if key == "commonName":
                    cns.add(value)

    # PyPI uses this one
    assert "DigiCert High Assurance EV Root CA" in cns

    # these CA should either be completely blocked or not on the trust list
    # for TLS (email-only or object sign-only)
    distrusted = {
        "Certum CA",
        "Chambers of Commerce Root",
        "D-TRUST Root CA 3 2013",
        "Global Chambersign Root",
        "SwissSign Platinum CA - G2",
        "Symantec Class 1 Public Primary Certification Authority - G4",
        "Symantec Class 1 Public Primary Certification Authority - G6",
        "Symantec Class 2 Public Primary Certification Authority - G4",
        "Symantec Class 2 Public Primary Certification Authority - G6",
        "VeriSign Class 2 Public Primary Certification Authority - G3",
    }
    intersection = cns.intersection(distrusted)
    assert not sorted(intersection)
