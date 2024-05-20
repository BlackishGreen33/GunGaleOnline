"""Test config"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture
def mock_path() -> Path: # type: ignore
    """Mock a path, and clean when unit test done."""
    with TemporaryDirectory() as temp_path:
        yield Path(temp_path)
