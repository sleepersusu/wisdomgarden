import sys
from pathlib import Path

# Add repo root to path so backend can import shopping_cart package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
