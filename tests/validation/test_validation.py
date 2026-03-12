import pytest

from lexcql import validate
from lexcql.parser import QueryParser
from lexcql.parser import QueryParserException
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


def test_validate_with_warnings_list():
    # "valid" queries (warnings are ok)
    assert validate('''lemma =/lang=deu/lang=deu "Stadt"''', return_errors=False) is True
    assert len(validate('''lemma =/lang=deu/lang=deu "Stadt"''', return_errors=True)) == 0

    # but if warnings are handled as errors, we have something returned
    assert validate('''lemma =/lang=deu/lang=deu "Stadt"''', return_errors=False, warnings_as_errors=True) is False
    assert len(validate('''lemma =/lang=deu/lang=deu "Stadt"''', return_errors=True, warnings_as_errors=True)) == 1


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


def test_validation_violation_basic_v0_3(parser: QueryParser):
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


def test_validation_violation_multiple_v0_3(parser: QueryParser):

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


def test_validation_violation_modifier_value_v0_3(parser: QueryParser):
    # lang relation modifier requires a value
    query = """lemma =/lang Apfel"""
    node = parser.parse(query)
    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Modifier 'lang' requires a relation value, e.g. 'lang=deu'.")
    assert exc.value.query_fragment == "/lang"

    # any other relation modifier does not support an extra relation+value
    query = """lemma =/respectCase=no apfel"""
    node = parser.parse(query)
    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Modifier 'respectCase' does not support any extra relation!")
    assert exc.value.query_fragment == "/respectCase=no"


def test_validation_violation_modifier_relation_v0_3(parser: QueryParser):
    # relation modifier with a relation not EQUALS "="
    query = """lemma = /lang<>deu apfel"""
    node = parser.parse(query)
    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match("Modifier 'lang' uses unspecified relation: '<>'!")
    assert exc.value.query_fragment == "/lang<>deu"


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


def test_validation_warning_def_v0_3(parser: QueryParser):
    query = """def = Banane"""
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(raise_at_first_violation=False, warnings_as_errors=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message == """Usage of legacy definition index 'def'. Please update to 'definition'."""
    assert validator.warnings[0].fragment == """def = Banane"""
    assert validator.warnings[0].type == "validation-warning"


def test_validation_warnings_v0_3(parser: QueryParser):
    query = "lemma = 'Banane'"
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message.startswith("""Search term "'Banane'" is enclosed with single quotes""")

    # quoting does not work with single quotes
    # "'das" is considered a single token
    query = "lemma = 'das alte Haus'"
    with pytest.raises(QueryParserException) as exc:
        node = parser.parse(query)
    assert exc.match(r"unable to parse query")
    assert len(parser.errors) == 1
    assert parser.errors[0].fragment == "lemma = 'das alte"

    query = 'lemma = "das alte Haus"'
    node = parser.parse(query)


def test_validation_warnings_for_custom_names_v0_3(parser: QueryParser):
    query = "lemma =/xlang=deu-de apfel"
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(allowed_modifiers=["xlang"], raise_at_first_violation=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message == "Custom modifier 'xlang' may not support any extra relation?"
    assert validator.warnings[0].fragment == "/xlang=deu-de"


def test_validation_warnings_for_modifiers_v0_3(parser: QueryParser):
    # duplicate modifiers
    query = "lemma =/lang=deu/lang=eng apfel"
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(raise_at_first_violation=True, warnings_as_errors=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message == "Relation '=' has duplicate modifier 'lang'?"
    assert validator.warnings[0].fragment == "=/lang=deu/lang=eng"

    # ------------------------------------------

    # mutually exclusive
    query = "lemma =/ignoreCASE/respectCase Apfel"
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(case_insensitive=True, raise_at_first_violation=True, warnings_as_errors=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message == (
        "Relation '=' uses mutually exclusive modifiers ['ignorecase', 'respectcase']"
        " (not allowed together ['ignoreCase', 'respectCase'])!"
    )
    assert validator.warnings[0].fragment == "=/ignoreCASE/respectCase"

    # ------------------------------------------

    # mutually exclusive and double
    query = "lemma =/ignoreCASE/respectCase/lang=deu/lang=deu Apfel"
    node = parser.parse(query)

    validator = LexCQLValidatorV0_3(case_insensitive=True, raise_at_first_violation=True, warnings_as_errors=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 2


# ---------------------------------------------------------------------------
