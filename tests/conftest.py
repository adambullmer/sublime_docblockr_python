from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture(autouse=True)
def sublime(request):
    mock = MagicMock()
    patcher = patch.dict('sys.modules', {
        'sublime': mock,
    })
    patcher.start()
    request.addfinalizer(patcher.stop)

    return mock


@pytest.fixture(autouse=True)
def sublime_plugin(request):
    mock = MagicMock()
    patcher = patch.dict('sys.modules', {
        'sublime_plugin': mock,
    })
    patcher.start()
    request.addfinalizer(patcher.stop)

    return mock


@pytest.fixture()
def root_commands():
    from .. import commands
    return commands


@pytest.fixture()
def root_DocblockrPython():
    from .. import DocblockrPython
    return DocblockrPython
