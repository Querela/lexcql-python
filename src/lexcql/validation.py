from abc import ABCMeta
from collections import deque
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional

from lexcql.parser import ErrorDetail
from lexcql.parser import Modifier
from lexcql.parser import QueryNode
from lexcql.parser import QueryVisitorAdapter
from lexcql.parser import Relation
from lexcql.parser import SearchClause

# ---------------------------------------------------------------------------


class SpecificationValidationError(Exception):
    def __init__(self, msg: str, node: QueryNode, query_fragment: Optional[str] = None, *args):
        super().__init__(msg, *args)
        self.node = node
        self.query_fragment = query_fragment


# TODO: create custom error classes for each error type? or add some type id?


class Validator(QueryVisitorAdapter[None], metaclass=ABCMeta):
    """An abstract base Validator for LexCQL queries.

    Subclasses should override the ``visit_`` QueryNode methods to
    implement the validation logic and use the ``.validation_error()``
    to raise/track validation errors.
    """

    def __init__(
        self,
        *,
        query: Optional[str] = None,
        case_insensitive: bool = True,
        raise_at_first_violation: bool = True,
    ):
        """Creates a LexCQL Validator that checks that only known indexes are used
        and that relations and relation modifiers are valid.

        Args:
            query: the original query string used for constructing the query node tree.
                   Used to provide more context for validation errors. Defaults to None.
            case_insensitive: Whether indexes (field names) are check case-insensitively.
                              Defaults to True.
            raise_at_first_violation: Raise a ``SpecificationValidationError`` at first
                                      conformance validation or try to gather as many infos
                                      as possible. Will be available in ``.errors`` attribute.
                                      Defaults to True.
        """
        super().__init__()

        self.query = query
        """query string to add context to error messages for better error locations"""

        self.case_insensitive = case_insensitive
        """Whether index/field name matching happens case-(in)sensitively"""

        self.raise_at_first_violation = raise_at_first_violation
        """Whether to raise at first violation."""
        self.errors: List[ErrorDetail] = list()
        """List of specification validation errors if ``.raise_at_first_violation`` is ``False``"""

    def validate(self, node: QueryNode, *, query: Optional[str] = None):
        """Validate parse query node tree.

        Args:
            node: the parsed query node (root of parse tree)
            query: the raw query input string. Will be used to add more context
                   to error messages by adding the fragment where the error was
                   caused. Defaults to None.

        Returns:
            bool: ``True`` if query in valid, ``False`` if any error was recorded
                  in the ``.errors`` attribute
        """
        # allows to override the query string here
        if query is not None:
            self.query = query

        # reset list of errors
        self.errors = []

        self.visit(node)

        return len(self.errors) == 0

    def is_valid(self, node: QueryNode, *, query: Optional[str] = None) -> bool:
        """Convenience method that simply calls ``.validate()`` and returns
        ``True`` if the query was valid.

        Args:
            node: the parsed query node (root of parse tree)
            query: the raw query input string. Will be used to add more context
                   to error messages by adding the fragment where the error was
                   caused. Defaults to None.

        Returns:
            bool: ``True`` if query in valid, ``False`` otherwise

        Note:
            The ``.errors`` attribute will not be used here as the first validation
            error will abort the validation process.
        """
        try:
            return self.validate(node, query=query)
        except SpecificationValidationError:
            return False

    def validation_error(self, node: QueryNode, error: str):
        """(Internal) Raises or tracks a new validation  error.

        Args:
            node: the query node where the validation error was caused
            error: the error message

        Raises:
            SpecificationValidationError: the raised error if ``.raise_at_first_violation``
                                          is set to ``True``
        """
        fragment = None
        if self.query and node.location:
            fragment = self.query[node.location.start : node.location.stop]  # noqa: E203

        if self.raise_at_first_violation:
            raise SpecificationValidationError(error, node, fragment)

        self.errors.append(
            ErrorDetail(
                message=error,
                type="validation-error",
                position=node.location,
                fragment=fragment,
            )
        )


# ---------------------------------------------------------------------------


class LexCQLValidatorV0_3(Validator):
    """LexCQL Query Validator for LexCQL Spec v0.3."""

    SPECIFICATION_VERSION = "0.3"
    """LexCQL specification version"""

    KNOWN_INDEXES = [
        "lang",
        "lemma",
        "entryId",
        "phonetic",
        "translation",
        "transcription",
        "definition",
        "etymology",
        "case",
        "number",
        "gender",
        "pos",
        "baseform",
        "segmentation",
        "sentiment",
        "frequency",
        "antonym",
        "hyponym",
        "hypernym",
        "meronym",
        "holonym",
        "synonym",
        "related",
        "ref",
        "senseRef",
        "citation",
    ]
    """List of LexCQL indexes (LexCQL field names)"""
    KNOWN_RELATIONS = ["=", "==", "is"]
    """List of LexCQL relations"""
    KNOWN_MODIFIERS = [
        "masked",
        "unmasked",
        "lang",
        "ignoreCase",
        "respectCase",
        "ignoreAccents",
        "respectAccents",
        "honorWhitespace",
        "regexp",
        "partialMatch",
        "fullMatch",
    ]
    """List of LexCQL relation modifiers"""

    def __init__(
        self,
        *,
        allowed_indexes: Optional[List[str]] = None,
        query: Optional[str] = None,
        case_insensitive: bool = True,
        raise_at_first_violation: bool = True,
    ):
        """Creates a LexCQL v0.3 Validator that checks that only known indexes are used
        and that relations and relation modifiers are valid.

        Args:
            allowed_indexes: Override the default ``KNOWN_INDEXES`` list of LexCQL field names.
                             Defaults to None.
            query: the original query string used for constructing the query node tree.
                   Used to provide more context for validation errors. Defaults to None.
            case_insensitive: Whether indexes (field names) are check case-insensitively.
                              Defaults to True.
            raise_at_first_violation: Raise a ``SpecificationValidationError`` at first
                                      conformance validation or try to gather as many infos
                                      as possible. Will be available in ``.errors`` attribute.
                                      Defaults to True.
        """

        super().__init__(
            query=query,
            case_insensitive=case_insensitive,
            raise_at_first_violation=raise_at_first_violation,
        )

        self.stack: Deque[QueryNode] = deque()
        """(internal) Query node stack to keep track of parents."""

        self.allowed_indexes = allowed_indexes
        """User-defined list of known indexes (LexCQL field names)"""

        if self.case_insensitive:
            # NOTE: overrides on instance (not on class level)
            self.KNOWN_INDEXES = list(map(str.lower, self.KNOWN_INDEXES))
            self.KNOWN_MODIFIERS = list(map(str.lower, self.KNOWN_MODIFIERS))

            if self.allowed_indexes:
                self.allowed_indexes = list(map(str.lower, self.allowed_indexes))

    # ----------------------------------------------------

    def visit_SearchClause(self, node: SearchClause):
        index = node.index
        if index:
            if self.case_insensitive:
                index = index.lower()
            if self.allowed_indexes:
                if index not in self.allowed_indexes:
                    self.validation_error(
                        node, f"Unknown index '{node.index}' (only allowed: {self.allowed_indexes!r})!"
                    )
            else:
                if index not in self.KNOWN_INDEXES:
                    self.validation_error(node, f"Unknown index '{node.index}'!")

        # TODO: check `search_term` against relations/modifiers? (regex/masked)

        self.stack.append(node)
        super().visit_SearchClause(node)
        self.stack.pop()

    def visit_Relation(self, node: Relation):
        #  parent = self.stack[-1]

        relation = node.relation
        if relation is not None:
            if self.case_insensitive:
                relation = relation.lower()
            if relation not in self.KNOWN_RELATIONS:
                self.validation_error(node, f"Relation '{node.relation}' is unspecified!")

            if relation == "is" and node.modifiers:
                self.validation_error(node, f"Relation '{node.relation}' does not support any modifiers!")

            # TODO: check modifiers that ignore/respect do not appear together
            # TODO: masked/unmasked/regex should not appear together

        self.stack.append(node)
        super().visit_Relation(node)
        self.stack.pop()

    def visit_Modifier(self, node: Modifier):
        #  parent = self.stack[-1]

        name = node.name
        if self.case_insensitive:
            name = name.lower()

        if name not in self.KNOWN_MODIFIERS:
            self.validation_error(node, f"Modifier '{node.name}' is unspecified!")

        # check against parent? --> visit_Relation "is" check

        relation = node.relation
        if relation and name != "lang":
            self.validation_error(node, f"Modifier '{node.name}' does not support any extra relation!")

        if relation and name == "lang":
            # TODO: do a valid language code check
            pass


# ---------------------------------------------------------------------------

VALIDATORS: Dict[str, Validator] = {
    LexCQLValidatorV0_3.SPECIFICATION_VERSION: LexCQLValidatorV0_3,
}
"""Mapping of all known LexCQL Validators. Uses the LexCQL specification
version as the key and returns the ``Validator`` class for instantiating."""

DEFAULT_VALIDATOR_SPECIFICATION_VERSION = LexCQLValidatorV0_3.SPECIFICATION_VERSION
"""The default LexCQL specification version for query validation."""

# ---------------------------------------------------------------------------
