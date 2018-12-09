import pytest


@pytest.fixture()
def formatter_base():
    from formatters import base
    return base


@pytest.fixture()
def formatter_docblock():
    from formatters import docblock
    return docblock


@pytest.fixture()
def formatter_google():
    from formatters import google
    return google


@pytest.fixture()
def formatter_numpy():
    from formatters import numpy
    return numpy


@pytest.fixture()
def formatter_PEP0257():
    from formatters import PEP0257
    return PEP0257


@pytest.fixture()
def formatter_registry():
    from formatters import registry
    return registry


@pytest.fixture()
def formatter_sphinx():
    from formatters import sphinx
    return sphinx


@pytest.fixture()
def formatter_utils():
    from formatters import utils
    return utils
