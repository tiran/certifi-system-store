import pytest

try:
    import requests
except ImportError:
    pytestmark = pytest.mark.skip


def test_requests():
    requests.get("https://pypi.org/")
