import pytest

from lexcql.parser import QueryParser

# ---------------------------------------------------------------------------


@pytest.fixture
def parser():
    """QueryParser"""

    return QueryParser()


# ---------------------------------------------------------------------------
