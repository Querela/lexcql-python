# LexCQL for Python

A query parser for LexCQL, the query language for lexical resources in the CLARIN Federated Content Search (FCS).

## Installation

Install from PyPI:

```bash
python3 -m pip install lexcql-parser
```

Or install from source:

```bash
git clone https://github.com/Querela/lexcql-python.git
cd lexcql-python
uv build

# built package
python3 -m pip install dist/lexcql_parser-<version>-py3-none-any.whl
# or
python3 -m pip install dist/lexcql_parser-<version>.tar.gz

# for local development
python3 -m pip install -e .
```

## Usage

The high-level interface `lexcql.parser.QueryParser` wraps the ANTLR4 parse tree into a simplified query node tree that is easier to work with. The `lexcql-parser` exposes a simple parsing function with `lexcql.parse(input: str, enableSourceLocations: bool = True) -> lexcql.parser.QueryNode`:

```python
import lexcql

## parsing a valid query into a query node tree
# our query input string
input = "Banane Or lemma =/lang=eng apple"
# parse into QueryNode tree
sc = lexcql.parse(input)
# print stringified tree
print(str(sc))

## handling possibly invalid queries
input = "broken query"
try:
    lexcql.parse(input)
except lexcql.QueryParserException as ex:
    print(f"Error: {ex}")
```

You can also use the more low-level ANTLR4 framework to parse the query string. A handy wrapper is provided with `lexcql.antlr_parse(input: str) -> LexParser.QueryContext`.

```python
from antlr4 import CommonTokenStream, InputStream
from lexcql.parser import LexLexer, LexParser

input = "example"
input_stream = InputStream(input)
lexer = LexLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = LexParser(stream)
tree: LexParser.QueryContext = parser.query()
```

Parsed queries can also be checked against their specification conformance.

```python
from lexcql import QueryParser
from lexcql.validation import LexCQLValidatorV0_3

parser = QueryParser(enableSourceLocations=True)

query = """Banane"""
node = parser.parse(query)
validator = LexCQLValidatorV0_3()
validator.validate(node, query=query)
len(validator.errors) == 0  # no errors

# or to raise an error on first violation
query = """post = NOUN"""
node = parser.parse(query)
validator = LexCQLValidatorV0_3(raise_at_first_violation=True)
validator.validate(node, query=query)  # raises SpecificationValidationError
```

A convenience method is provded with `lexcql.validate(query: str)`:

```python
from lexcql import validate

# simple boolean returns
validate("lemma = apple")  # => True
validate("lemmas = apple")  # => False ("lemmas" is unknown field name)
validate("lemma =")  # => False (parse error, missing search term)

# or with list of errors
error = validate("post = NOUN", return_errors=True)[0]  # has one error
assert error.message == "Unknown index 'post'!"
# error is the full query
assert error.fragment == "post = NOUN"
assert error.position.start == 0
assert error.position.stop == 11
assert error.type == "validation-error"
```

## Development

Fetch (or update) grammar files:

```bash
git clone https://github.com/clarin-eric/fcs-ql.git
cp fcs-ql/src/main/antlr4/eu/clarin/sru/fcs/qlparser/lex/*.g4 src/lexcql/
```

(Re-)Generate python parser code:

```bash
# setup environment
uv sync --extra antlr
# NOTE: you can activate the environment (if you do not want to prefix everything with `uv run`)
# NOTE: `uv` does not play nicely with `pyenv` - if you use `pyenv`, sourcing does NOT work!
source .venv/bin/activate

cd src/lexcql
uv run antlr4 -Dlanguage=Python3 *.g4 -listener -visitor
```

Run style checks:

```bash
# setup environment
uv sync --extra style

uv run black --check .
uv run flake8 . --show-source --statistics
uv run isort --check --diff .
```

Run tests:

```bash
# setup environment
uv sync --extra test

uv run pytest
# to see output and run a specific test file
uv run pytest -v -rP tests/validation/test_validation.py
```

Run check before publishing:

```bash
# setup environment
uv sync --extra build

# build the package
uv build
# run metadata check
uv run twine check --strict dist/*
# (manual) check of package contents
tar tvf dist/lexcql_parser-*.tar.gz
```

## See also

- [clarin-eric/fcq-ql](https://github.com/clarin-eric/fcs-ql) - FCS-QL/LexCQL Parser (Java)
- [Querela/fcs-ql-python](https://github.com/Querela/fcs-ql-python) - FCS-QL Parser (Python)
- [Specification on CLARIN FCS 2](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details) - CLARIN FCS Overview
- [Specification on LexFCS](https://doi.org/10.5281/zenodo.7849753) - Published LexFCS Specification
