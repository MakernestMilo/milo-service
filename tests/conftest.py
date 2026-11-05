import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from milo.app import create_app  # noqa: E402
from milo.levels import load_all  # noqa: E402
from milo.model import FakeModel  # noqa: E402
from milo.store import MemoryStore  # noqa: E402

LEVELS = load_all()
SID = "s" * 32


@pytest.fixture
def levels():
    return LEVELS


@pytest.fixture
def origins():
    return LEVELS["origins"]


@pytest.fixture
def model():
    return FakeModel()


@pytest.fixture
def app(model):
    return create_app(model=model, store=MemoryStore(), levels=LEVELS, env={"PANEL_TOKEN": "t" * 24})


@pytest.fixture
def client(app):
    return TestClient(app)
