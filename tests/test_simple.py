import os

import certifi
import pkg_resources


def test_where():
    assert os.path.isfile(certifi.where())


def test_contents():
    contents = certifi.contents()
    assert "BEGIN CERTIFICATE" in contents


def test_is_css():
    assert certifi.__certifi_system_trust__


def test_version():
    for distname in ("certifi", "certifi_system_store"):
        dist = pkg_resources.get_distribution(distname)
        assert dist.version.startswith("30")
