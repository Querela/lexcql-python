import pytest

from lexcql import validate
from lexcql.parser import QueryParser
from lexcql.parser import SourceLocation
from lexcql.validation import LexCQLValidatorV0_3
from lexcql.validation import SpecificationValidationError

# ---------------------------------------------------------------------------


@pytest.fixture
def parser():
    """Query Parser with ``SourceLocation``s enabled.

    Returns:
        QueryParser: the query parser for parsing query strings
    """
    return QueryParser(enableSourceLocations=True)


# ---------------------------------------------------------------------------
# test convenience validate method


def test_validate():
    # valid queries
    assert validate("Banane") is True
    assert validate("lemma = Banane") is True
    assert validate("pos == NOUN") is True
    assert validate('''pos == NOUN or lemma =/lang=deu "Stadt"''') is True

    # invalid (invalid indexes)
    assert validate("post == NOUN") is False
    assert validate("lemmas = Banane") is False
    assert validate("doesnotexist = Banane") is False

    # invalid (parse errors)
    assert validate("pos ==") is False
    assert validate("lemma is apple pie") is False

    # with specific version number
    assert validate("pos = NOUN", version="0.3") is True
    assert validate("post == NOUN", version="0.3") is False


def test_validate_with_errors_list():
    # valid queries
    assert len(validate("Banane", return_errors=True)) == 0
    assert len(validate('''pos == NOUN or lemma =/lang=deu "Stadt"''', return_errors=True)) == 0

    # invalid queries (parse error)
    errors = validate("die Banane", return_errors=True)
    assert len(errors) == 1
    assert errors[0].fragment == "die Banane"
    # indicates end of string (missing something)
    assert errors[0].position == SourceLocation(start=10, stop=10)
    assert errors[0].message == """missing {QUOTED_STRING, SIMPLE_STRING} at '<EOF>'"""

    # invalid queries (validation error)
    errors = validate("post = NOUN", return_errors=True)
    assert len(errors) == 1
    assert errors[0].fragment == "post = NOUN"
    assert errors[0].position == SourceLocation(start=0, stop=11)  # full query
    assert errors[0].message == "Unknown index 'post'!"


# ---------------------------------------------------------------------------
# test for LexCQL v0.3


def test_validation_basic_v0_3(parser: QueryParser):
    query = """Banane"""
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3()
    assert validator.query is None

    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # create validator with a query string (which might not be the real one)
    validator = LexCQLValidatorV0_3(query="test")
    assert validator.query == "test"
    # the query will be overwritten in the .validate() method
    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # repeated calls should reset correctly
    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # convenience method
    assert validator.is_valid(node) is True
    assert validator.query == query
    assert not validator.errors


def test_validation_basic_with_violation_v0_3(parser: QueryParser):
    query = """doesnotexist = Banane"""
    node = parser.parse(query)

    # fail on first violation
    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Unknown index 'doesnotexist'!")
    assert exc.value.query_fragment == query

    # or we can record violations
    validator = LexCQLValidatorV0_3(raise_at_first_violation=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 1
    assert validator.errors[0].fragment == query

    # reset .errors list
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 1

    # ------------------------------------------

    # context fragment is not whole query
    query = """Apfel OR doesnotexist = Banane"""
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Unknown index 'doesnotexist'!")
    assert exc.value.query_fragment == """doesnotexist = Banane"""

    # ------------------------------------------

    query = '''doesnotexist = Banane AND alsoinvalid = "grüner Apfel"'''
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Unknown index 'doesnotexist'!")
    assert exc.value.query_fragment == """doesnotexist = Banane"""
    assert len(validator.errors) == 0

    validator = LexCQLValidatorV0_3(raise_at_first_violation=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 2
    assert validator.errors[0].message == "Unknown index 'doesnotexist'!"
    assert validator.errors[0].fragment == """doesnotexist = Banane"""
    assert validator.errors[1].message == "Unknown index 'alsoinvalid'!"
    assert validator.errors[1].fragment == '''alsoinvalid = "grüner Apfel"'''


def test_validation_custom_index_v0_3(parser: QueryParser):
    query = """doesnotexist = Banane"""
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(allowed_indexes=["doesnotexist"], raise_at_first_violation=True)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True

    # otherwise correct query with spec conform fields (indexes)
    query = """lemma = Banane"""
    node = parser.parse(query)

    # NOTE: do not do this unless strictly necessary!
    validator = LexCQLValidatorV0_3(allowed_indexes=["doesnotexist"], raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Unknown index 'lemma' \(only allowed: \['doesnotexist'\]\)!")
    assert exc.value.query_fragment == query

    # while normally
    validator = LexCQLValidatorV0_3(allowed_indexes=None, raise_at_first_violation=True)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True


# ---------------------------------------------------------------------------
