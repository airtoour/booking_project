import pytest
from app.database import engine


@pytest.fixture
def prepare_database():
    assert ...