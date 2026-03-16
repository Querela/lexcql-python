import pytest

from lexcql.parser import QueryParser

# ---------------------------------------------------------------------------


@pytest.fixture
def parser_with_locations():
    """Query Parser with ``SourceLocation``s enabled.

    Returns:
        QueryParser: the query parser for parsing query strings
    """

    return QueryParser(enableSourceLocations=True)


# ---------------------------------------------------------------------------


def test_search_clause_quoted(parser: QueryParser):
    query = '''"House of Dragons"'''
    tree = parser.parse(query)
    assert str(tree) == "(SearchClause House of Dragons [quoted])"

    query = '"cat"'
    tree = parser.parse(query)
    assert str(tree) == "(SearchClause cat [quoted])"

    query = "cat"
    tree = parser.parse(query)
    assert str(tree) == "(SearchClause cat)"

    query = 'lemma = "cat"'
    tree = parser.parse(query)
    assert str(tree) == "(SearchClause lemma (Relation =) cat [quoted])"


# ---------------------------------------------------------------------------
