from abc import ABCMeta
from collections import deque
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar

from lexcql.parser import ErrorDetail
from lexcql.parser import Modifier
from lexcql.parser import QueryNode
from lexcql.parser import QueryVisitorAdapter
from lexcql.parser import Relation
from lexcql.parser import SearchClause
from lexcql.parser import SearchClauseGroup
from lexcql.parser import Subquery

# ---------------------------------------------------------------------------

_R = TypeVar("_R")

# ---------------------------------------------------------------------------


class SpecificationValidationError(Exception):
    def __init__(self, msg: str, node: QueryNode, query_fragment: Optional[str] = None, *args):
        super().__init__(msg, *args)
        self.node = node
        self.query_fragment = query_fragment


# TODO: create custom error classes for each error type? or add some type id?


class Validator(QueryVisitorAdapter[_R], metaclass=ABCMeta):
    """An abstract base Validator for LexCQL queries.

    Subclasses should override the ``visit_`` QueryNode methods to
    implement the validation logic and use the ``.validation_error()``
    to raise/track validation errors and ``.validation_warning()`` for
    warnings (may also raise errors depending on configuration).
    """

    def __init__(
        self,
        *,
        query: Optional[str] = None,
        case_insensitive: bool = True,
        raise_at_first_violation: bool = True,
        warnings_as_errors: bool = False,
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
            warnings_as_errors: Handle warnings the same as errors. May raise ``SpecificationValidationError``.
        """
        super().__init__()

        self.stack: Deque[QueryNode] = deque()
        """(internal) Query node stack to keep track of query node parents."""

        self.query = query
        """query string to add context to error messages for better error locations"""

        self.case_insensitive = case_insensitive
        """Whether index/field name matching happens case-(in)sensitively"""

        self.raise_at_first_violation = raise_at_first_violation
        """Whether to raise at first violation."""
        self.warnings_as_errors = warnings_as_errors
        """Whether to handle warnings the same as errors."""
        self.errors: List[ErrorDetail] = list()
        """List of specification validation errors if ``.raise_at_first_violation`` is ``False``"""
        self.warnings: List[ErrorDetail] = list()
        """List of warnings about not-quite-violations of the specification but bad practice or
        what can be unexpected results."""

    def validate(self, node: QueryNode, *, query: Optional[str] = None):
        """Validate parse query node tree.

        Args:
            node: the parsed query node (root of parse tree)
            query: the raw query input string. Will be used to add more context
                   to error messages by adding the fragment where the error was
                   caused. Defaults to None.

        Returns:
            bool: ``True`` if query in valid, ``False`` if any error was recorded
                  in the ``.errors`` attribute (or in ``.warnings`` if ``.warnings_as_errors``)
        """
        # allows to override the query string here
        if query is not None:
            self.query = query

        # reset list of errors
        self.errors = []
        self.warnings = []

        self.visit(node)

        num_issues = len(self.errors)
        if self.warnings_as_errors:
            num_issues += len(self.warnings)

        return num_issues == 0

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

    def validation_error(self, node: QueryNode, message: str):
        """(Internal) Raises or tracks a new validation error.

        Args:
            node: the query node where the validation error was caused
            message: the error message

        Raises:
            SpecificationValidationError: the raised error if ``.raise_at_first_violation``
                                          is set to ``True``
        """
        fragment = None
        if self.query and node.location:
            fragment = self.query[node.location.start : node.location.stop]  # noqa: E203

        if self.raise_at_first_violation:
            raise SpecificationValidationError(message, node, fragment)

        self.errors.append(
            ErrorDetail(
                message=message,
                type="validation-error",
                position=node.location,
                fragment=fragment,
            )
        )

    def validation_warning(self, node: QueryNode, message: str):
        """(Internal) Tracks validation warnings.

        If ``.warnings_as_errors`` is ``True`` and ``.raise_at_first_violation``
        is ``True``, it will raise ``SpecificationValidationError``.

        Args:
            node: the query node where the validation error was caused
            message: the error message

        Raises:
            SpecificationValidationError: the raised error if ``.raise_at_first_violation``
                                          and ``.warnings_as_errors`` are set to ``True``
        """
        fragment = None
        if self.query and node.location:
            fragment = self.query[node.location.start : node.location.stop]  # noqa: E203

        if self.warnings_as_errors:
            if self.raise_at_first_violation:
                raise SpecificationValidationError(message, node, fragment)

        self.warnings.append(
            ErrorDetail(
                message=message,
                type="validation-warning",
                position=node.location,
                fragment=fragment,
            )
        )

    # ----------------------------------------------------

    @property
    def parent_node(self) -> Optional[QueryNode]:
        """Get the current parent ``QueryNode`` or ``None`` if unavailable.

        Intended to be used in the ``visit_`` ``QueryNode`` handlers.

        Returns:
            Optional[QueryNode]: the parent query node or ``None``
        """
        if self.stack:
            return self.stack[-1]
        return None

    def visit_Subquery(self, node: Subquery) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_Subquery(node)
        self.stack.pop()
        return result

    def visit_SearchClauseGroup(self, node: SearchClauseGroup) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_SearchClauseGroup(node)
        self.stack.pop()
        return result

    def visit_SearchClause(self, node: SearchClause) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_SearchClause(node)
        self.stack.pop()
        return result

    def visit_Relation(self, node: Relation) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_Relation(node)
        self.stack.pop()
        return result

    def visit_Modifier(self, node: Modifier) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_Modifier(node)
        self.stack.pop()
        return result


# ---------------------------------------------------------------------------


class LexCQLValidatorV0_3(Validator[None]):
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
    MUTUALLY_EXCLUSIVE_MODIFIERS = [
        # TODO: masked/unmasked/regex ?
        {"masked", "unmasked"},
        {"ignoreCase", "respectCase"},
        {"ignoreAccents", "respectAccents"},
        {"partialMatch", "fullMatch"},
    ]
    """List of mutually exclusive relation modifiers. They should not appear together."""

    def __init__(
        self,
        *,
        allowed_indexes: Optional[List[str]] = None,
        allowed_modifiers: Optional[List[str]] = None,
        query: Optional[str] = None,
        case_insensitive: bool = True,
        raise_at_first_violation: bool = True,
        warnings_as_errors: bool = False,
    ):
        """Creates a LexCQL v0.3 Validator that checks that only known indexes are used
        and that relations and relation modifiers are valid.

        Args:
            allowed_indexes: Override the default ``KNOWN_INDEXES`` list of LexCQL field names.
                             Defaults to None.
            allowed_modifiers: Override the default ``KNOWN_MODIFIERS`` list of LexCQL
                               relation modifiers. Defaults to None.
            query: the original query string used for constructing the query node tree.
                   Used to provide more context for validation errors. Defaults to None.
            case_insensitive: Whether indexes (field names) are check case-insensitively.
                              Defaults to True.
            raise_at_first_violation: Raise a ``SpecificationValidationError`` at first
                                      conformance validation or try to gather as many infos
                                      as possible. Will be available in ``.errors`` attribute.
                                      Defaults to True.
            warnings_as_errors: Handle warnings the same as errors. May raise ``SpecificationValidationError``.
        """

        super().__init__(
            query=query,
            case_insensitive=case_insensitive,
            raise_at_first_violation=raise_at_first_violation,
            warnings_as_errors=warnings_as_errors,
        )

        self.allowed_indexes = allowed_indexes
        """User-defined list of known indexes (LexCQL field names)"""
        self.allowed_modifiers = allowed_modifiers
        """User-defined list of known modifiers (LexCQL relation modifiers)"""

        if self.case_insensitive:
            # NOTE: overrides on instance (not on class level)
            self.KNOWN_INDEXES = list(map(str.lower, self.KNOWN_INDEXES))
            self.KNOWN_RELATIONS = list(map(str.lower, self.KNOWN_RELATIONS))
            self.KNOWN_MODIFIERS = list(map(str.lower, self.KNOWN_MODIFIERS))
            self.MUTUALLY_EXCLUSIVE_MODIFIERS = [set(map(str.lower, ms)) for ms in self.MUTUALLY_EXCLUSIVE_MODIFIERS]

            if self.allowed_indexes:
                self.allowed_indexes = list(map(str.lower, self.allowed_indexes))
            if self.allowed_modifiers:
                self.allowed_modifiers = list(map(str.lower, self.allowed_modifiers))
                # TODO: update self.MUTUALLY_EXCLUSIVE_MODIFIERS?

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
                    if index == "def":
                        self.validation_warning(
                            node, f"Usage of legacy definition index '{node.index}'. Please update to 'definition'."
                        )
                    else:
                        self.validation_error(node, f"Unknown index '{node.index}'!")

        # TODO: check `search_term` against relations/modifiers? (regex/masked)

        # warn about single quotes (not working being quotes?)
        search_term = node.search_term
        if search_term.startswith("'") and search_term.endswith("'"):
            self.validation_warning(
                node,
                (
                    f"Search term {search_term!r} is enclosed with single quotes [']."
                    ' Single quotes are not used quoting, only double qoutes ["]!'
                    " Endpoint may include the literal single quote when searching."
                ),
            )

        super().visit_SearchClause(node)

    def visit_Relation(self, node: Relation):
        #  parent = self.stack[-1]

        relation = node.relation
        if self.case_insensitive:
            relation = relation.lower()
        if relation not in self.KNOWN_RELATIONS:
            self.validation_error(node, f"Relation '{node.relation}' is unspecified!")

        # check modifiers
        if node.modifiers:
            if relation == "is":
                self.validation_error(node, f"Relation '{node.relation}' does not support any modifiers!")
            # TODO: relation == "==", what modifiers make sense here?

            # check duplicate modifiers (should not be useful in any scenario imaginable)
            modifier_names: Set[str] = set()
            for modifier in node.modifiers:
                modifier_name = modifier.name
                if self.case_insensitive:
                    modifier_name = modifier_name.lower()
                if modifier_name in modifier_names:
                    self.validation_warning(
                        node, f"Relation '{node.relation}' has duplicate modifier '{modifier.name}'?"
                    )
                modifier_names.add(modifier_name)

            # check modifiers that ignore/respect do not appear together
            if len(modifier_names) >= 2:
                for i, excl_set in enumerate(self.MUTUALLY_EXCLUSIVE_MODIFIERS):
                    intersection = excl_set & modifier_names
                    if len(intersection) > 1:
                        self.validation_warning(
                            node,
                            (
                                f"Relation '{node.relation}' uses mutually exclusive modifiers"
                                f" {sorted(modifier_names)!r} (not allowed together "
                                f"{sorted(LexCQLValidatorV0_3.MUTUALLY_EXCLUSIVE_MODIFIERS[i])!r})!"
                            ),
                        )

        super().visit_Relation(node)

    def visit_Modifier(self, node: Modifier):
        #  parent = self.stack[-1]

        name = node.name
        if self.case_insensitive:
            name = name.lower()
        if self.allowed_modifiers:
            if name not in self.allowed_modifiers:
                self.validation_error(
                    node, f"Unknown modifier '{node.name}' (only allowed: {self.allowed_modifiers!r})!"
                )
        else:
            if name not in self.KNOWN_MODIFIERS:
                self.validation_error(node, f"Modifier '{node.name}' is unspecified!")

        # check against parent? --> visit_Relation "is" check

        relation = node.relation
        if relation and name != "lang":
            if self.allowed_modifiers and name in self.allowed_modifiers and name not in self.KNOWN_MODIFIERS:
                self.validation_warning(node, f"Custom modifier '{node.name}' may not support any extra relation?")
            else:
                self.validation_error(node, f"Modifier '{node.name}' does not support any extra relation!")

        if not relation and name == "lang":
            self.validation_error(node, f"Modifier '{node.name}' requires a relation value, e.g. 'lang=deu'.")

        if relation and relation != "=":
            self.validation_error(node, f"Modifier '{node.name}' uses unspecified relation: {relation!r}!")

        # TODO: check valid `node.value` for lang modifier?


# ---------------------------------------------------------------------------

VALIDATORS: Dict[str, Type[Validator]] = {
    LexCQLValidatorV0_3.SPECIFICATION_VERSION: LexCQLValidatorV0_3,
}
"""Mapping of all known LexCQL Validators. Uses the LexCQL specification
version as the key and returns the ``Validator`` class for instantiating."""

DEFAULT_VALIDATOR_SPECIFICATION_VERSION = LexCQLValidatorV0_3.SPECIFICATION_VERSION
"""The default LexCQL specification version for query validation."""

# ---------------------------------------------------------------------------
