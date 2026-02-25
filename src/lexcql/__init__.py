from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from lexcql.parser import LexLexer
from lexcql.parser import LexParser
from lexcql.parser import LexParserListener  # noqa: F401
from lexcql.parser import QueryNode
from lexcql.parser import QueryParser
from lexcql.parser import QueryParserException  # noqa: F401

# ---------------------------------------------------------------------------


class SyntaxError(Exception):
    pass


class ExceptionThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"line {line}:{column} {msg}")


def antlr_parse(input: str) -> LexParser.QueryContext:
    input_stream = InputStream(input)
    lexer = LexLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LexParser(stream)
    parser.addErrorListener(ExceptionThrowingErrorListener())
    tree: LexParser.QueryContext = parser.query()
    return tree


# ---------------------------------------------------------------------------


def parse(input: str, enableSourceLocations: bool = True) -> QueryNode:
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
    """Simple wrapper to check if the input string can be sucsessfully parsed.

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
