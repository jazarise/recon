import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope='session', autouse=True)
def mock_global_dependencies(monkeypatch):
    '''Mock global dependencies like database and networks to ensure isolated testing'''
    pass