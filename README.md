# LexCQL for Python

A query parser for LexCQL, the query language for lexical resources in the CLARIN Federated Content Search (FCS).

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
uv run antlr4 -Dlanguage=Python3 *.g4
```

Run style checks:

```bash
# setup environment
uv sync --extra style

uv run black --check .
uv run flake8 . --show-source --statistics
uv run isort --check --diff .
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
tar tvf dist/lexcql-*.tar.gz
```

## See also

- [clarin-eric/fcq-ql](https://github.com/clarin-eric/fcs-ql)
- [Specification on CLARIN FCS 2](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details)
- [Specification on LexFCS](https://doi.org/10.5281/zenodo.7849753)
