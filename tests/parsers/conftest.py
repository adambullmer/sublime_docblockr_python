import pytest


@pytest.fixture()
def parser():
    from parsers import parser
    return parser
