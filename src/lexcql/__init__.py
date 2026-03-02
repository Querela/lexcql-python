from typing import List
from typing import Literal
from typing import overload

from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from lexcql.LexLexer import LexLexer
from lexcql.LexParser import LexParser
from lexcql.LexParserListener import LexParserListener  # noqa: F401
from lexcql.LexParserVisitor import LexParserVisitor  # noqa: F401
from lexcql.parser import ErrorDetail
from lexcql.parser import QueryNode
from lexcql.parser import QueryParser
from lexcql.parser import QueryParserException  # noqa: F401
from lexcql.parser import SourceLocation  # noqa: F401
from lexcql.validation import DEFAULT_VALIDATOR_SPECIFICATION_VERSION
from lexcql.validation import VALIDATORS
from lexcql.validation import SpecificationValidationError

# ---------------------------------------------------------------------------


class SyntaxError(Exception):
    pass


class ExceptionThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"line {line}:{column} {msg}")


def antlr_parse(input: str) -> LexParser.QueryContext:
    """Run the low-level ANTLR4 tokenization and parsing. This returns the parsing
    context ANTLR4 uses instead of the simplified LexCQL query node types.

    Args:
        input: raw query string

    Returns:
        LexParser.QueryContext: the ANTLR4 root parsing context (query)

    Throws:
        SyntaxError: if an error occurred while parsing
    """
    input_stream = InputStream(input)
    lexer = LexLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LexParser(stream)
    parser.addErrorListener(ExceptionThrowingErrorListener())
    tree: LexParser.QueryContext = parser.query()
    return tree


# ---------------------------------------------------------------------------


def parse(input: str, *, enableSourceLocations: bool = True) -> QueryNode:
    """Simple wrapper to generate a `QueryParser` and to parse some
    input string into a `QueryNode`.

    Args:
        input: raw input query string
        enableSourceLocations: whether source locations are computed for each query node

    Returns:
        QueryNode: parsed query

    Throws:
        QueryParserException: if an error occurred
    """
    parser = QueryParser(enableSourceLocations=enableSourceLocations)
    return parser.parse(input)


def can_parse(input: str):
    """Simple wrapper to check if the input string can be successfully parsed.

    Args:
        input: raw input query string

    Returns:
        bool: ``True`` if query can be parsed, ``False`` otherwise.
    """
    try:
        parse(input)
        return True
    except QueryParserException:
        return False


# ---------------------------------------------------------------------------


@overload
def validate(
    input: str,
    *,
    version: str = DEFAULT_VALIDATOR_SPECIFICATION_VERSION,
    return_errors: Literal[False] = False,
    case_insensitive: bool = True,
    warnings_as_errors: bool = False,
) -> bool: ...


@overload
def validate(
    input: str,
    *,
    version: str = DEFAULT_VALIDATOR_SPECIFICATION_VERSION,
    return_errors: Literal[True] = True,
    case_insensitive: bool = True,
    warnings_as_errors: bool = False,
) -> List[ErrorDetail]: ...


def validate(
    input: str,
    *,
    version: str = DEFAULT_VALIDATOR_SPECIFICATION_VERSION,
    return_errors: bool = False,
    case_insensitive: bool = True,
    warnings_as_errors: bool = False,
):
    """Validate input query string by trying to parse it and if successful run a LexCQL
    specification validation. Collect errors/warnings.

    Args:
        input: the raw query input string
        version: the specification version to validate against.
                 Defaults to DEFAULT_VALIDATOR_SPECIFICATION_VERSION ("0.3").
        return_errors: whether to return simply a boolean if valid or a list of errors.
                       Defaults to False.
        case_insensitive: how to handle keywords/indexes in LexCQL. Defaults to True.
        warnings_as_errors: handle warnings as errors. Defaults to False.

    Raises:
        ValueError: raised if ``version`` argument specifies an unknown LexCQL specification
                    or no ``Validator`` can be found for this version.

    Returns:
        bool: if ``return_errors`` is ``False`` only return a boolean.
              Returns ``True`` if parsing and validation is without issues, ``False`` otherwise.
        List[ErrorDetail]: if ``return_errors`` is ``True`` return a list of errors AND warnings.
    """
    # "check" params
    validator_cls = VALIDATORS.get(version, None)
    if validator_cls is None:
        raise ValueError(f"No validator found for {version=}!")

    # create parser/validator
    parser = QueryParser(enableSourceLocations=True)
    validator = validator_cls(
        query=input,
        case_insensitive=case_insensitive,
        raise_at_first_violation=not return_errors,
        warnings_as_errors=warnings_as_errors,
    )

    # try to parse the input query string
    try:
        qn = parser.parse(input)
    except QueryParserException as ex:
        if not return_errors:
            return False

        errors = []
        if not str(ex).startswith("unable to parse query: "):
            errors.append(ErrorDetail(str(ex)))
        errors.extend(parser.errors)
        return errors

    # if parsing successful, run validation
    try:
        validator.validate(qn)
    except SpecificationValidationError:
        # not will raise if raise_at_first_violation enabled
        return False

    errors = list()
    errors.extend(validator.errors)
    if warnings_as_errors:
        errors.extend(validator.warnings)

    return errors if return_errors else not bool(errors)


# ---------------------------------------------------------------------------
