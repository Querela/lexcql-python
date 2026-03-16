import pytest

from lexcql.parser import QueryParser

# ---------------------------------------------------------------------------


@pytest.fixture
def parser():
    """Query Parser (with default configuration).

    Returns:
        QueryParser: the query parser for parsing query strings
    """

    return QueryParser()


# ---------------------------------------------------------------------------
