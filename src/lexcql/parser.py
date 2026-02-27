import logging
from abc import ABCMeta
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Deque
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import antlr4
import antlr4.error.ErrorListener
from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext
from antlr4 import Token
from antlr4.Recognizer import Recognizer
from antlr4.tree.Tree import TerminalNodeImpl

from lexcql.LexLexer import LexLexer
from lexcql.LexParser import LexParser
from lexcql.LexParserVisitor import LexParserVisitor

# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)

_T = TypeVar("_T", bound="QueryNode")
_R = TypeVar("_R")

# ---------------------------------------------------------------------------


class QueryNodeType(str, Enum):
    """Node types of LexCQL expression tree nodes."""

    def __str__(self) -> str:
        return self.value

    SEARCH_CLAUSE_GROUP = "SearchClauseGroup"
    """search clause group (either nested search clause groups or search clauses, with binary boolean relation)"""
    SUBQUERY = "Subquery"
    """subquery (either with nested query/search_clause_group in parentheses) or a search_clause"""
    SEARCH_CLAUSE = "SearchClause"
    """search clause"""
    RELATION = "Relation"
    """relation"""
    MODIFIER = "Modifier"
    """modifier"""


class RBoolean(str, Enum):
    """LexCQL expression tree boolean."""

    def __str__(self) -> str:
        return self.value

    AND = "AND"
    """logical 'and'"""
    OR = "OR"
    """logical 'or'"""
    NOT = "NOT"
    """logical 'and not'"""


# ---------------------------------------------------------------------------


class QueryVisitor(Generic[_R], metaclass=ABCMeta):
    """Interface implementing a Visitor pattern for LexCQL expression trees.

    Default method implementations do nothing.
    """

    def visit(self, node: "QueryNode") -> Optional[_R]:
        """Visit a query node. Generic handler, dispatches to visit methods
        based on `QueryNodeType` if exists else do nothing::

            method = "visit_" + node.node_type.value

        Args:
            node: the node to visit

        Returns:
            _R: visitation result or ``None`` (see `defaultResult()`)
        """
        if not node:
            return None

        def noop(node: "QueryNode") -> Optional[_R]:
            return self.defaultResult()

        # search for specific visit function based on node_type
        method_name = f"visit_{node.node_type}"
        method = getattr(self, method_name, noop)

        return method(node)

    # ----------------------------------------------------
    # same as antlr4.tree.Tree.ParseTreeVisitor

    def visitChildren(self, node: "QueryNode") -> _R:
        result = self.defaultResult()
        for i in range(node.child_count):
            if not self.shouldVisitNextChild(node, result):
                return result

            child = node.get_child(i)
            assert child is not None, f"child#{i} must not be None in {node=}"
            childResult = child.accept(self)
            result = self.aggregateResult(result, childResult)

        return result

    def defaultResult(self) -> Optional[_R]:
        return None

    def aggregateResult(self, aggregate: _R, nextResult: _R) -> _R:
        return nextResult

    def shouldVisitNextChild(self, node: "QueryNode", currentResult: _R) -> bool:
        return True


class QueryVisitorAdapter(QueryVisitor[_R]):
    """This class provides an empty implementation of ``QueryVisitor``,
    which can be extended to create a visitor which only needs to handle
    a subset of the available methods.

    Generic with regards to the return type of the visit operation.
    """

    def visit_SearchClauseGroup(self, node: "SearchClauseGroup") -> _R:
        """Visit a *search_clause_group* query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_Subquery(self, node: "Subquery") -> _R:
        """Visit a *subquery* query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_SearchClause(self, node: "SearchClause") -> _R:
        """Visit a *search_clause* query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_Relation(self, node: "Relation") -> _R:
        """Visit a *relation* query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_Modifier(self, node: "Modifier") -> _R:
        """Visit a *modifier* query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)


# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceLocation:
    """Source information wrapping start and stop offsets in the query text for a query node."""

    start: int
    """Start offset in raw query string"""
    stop: int
    """End offset in raw query string"""

    @staticmethod
    def fromContext(ctx: ParserRuleContext):
        if not ctx:
            return None

        # start and stop tokens might be null (maybe due to errors)
        if ctx.start is None or ctx.stop is None:
            return None

        start = ctx.start.start
        stop = ctx.stop.stop + 1
        # NOTE: stop+1 for Java/Python string indexing
        return SourceLocation(start, stop)

    @staticmethod
    def fromToken(tok: Token):
        if tok.start is None or tok.start == -1:
            return None
        if tok.stop is None or tok.stop == -1:
            return None

        start = tok.start
        stop = tok.stop + 1
        # NOTE: stop+1 for Java/Python string indexing
        return SourceLocation(start, stop)

    def __str__(self):
        return f"{self.start}:{self.stop}"


class QueryNode(metaclass=ABCMeta):
    """Base class for LexCQL expression tree nodes."""

    def __init__(
        self,
        node_type: QueryNodeType,
        *,
        children: Optional[List["QueryNode"]] = None,
        child: Optional["QueryNode"] = None,
        location: Optional[SourceLocation] = None,
    ):
        """[Constructor]

        Args:
            node_type: the type of the node
            children: the children of this node or ``None``. Defaults to None.
            child: the child of this node or ``None``. Defaults to None.
            location: the source code location for this query node
                      in the query text content or ``None``. Defaults to None.
        """
        self.node_type = node_type
        """The node type of this node."""

        self.parent: Optional[QueryNode] = None
        """The parent node of this node.

        ``None`` if this is the root node.
        """

        if not children:
            children = list()

        self.children = list(children)
        """The children of this node."""

        if child:
            self.children.append(child)

        # update parents in children
        for child in self.children:
            child.parent = self

        self.location: Optional[SourceLocation] = location
        """source location information about start/stop offsets for this query node in the query text content"""

    def has_node_type(self, node_type: QueryNodeType) -> bool:
        """Check, if node if of given type.

        Args:
            node_type: type to check against

        Returns:
            bool: ``True`` if node is of given type, ``False`` otherwise

        Raises:
            TypeError: if node_type is ``None``
        """
        if node_type is None:
            raise TypeError("node_type is None")
        return self.node_type == node_type

    @property
    def child_count(self) -> int:
        """Get the number of children of this node.

        Returns:
            int: the number of children of this node
        """
        return len(self.children) if self.children else 0

    def get_child(self, idx: int, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get a child node of specified type by index.

        When supplied with ``clazz`` parameter, only child nodes of
        the requested type are counted.

        Args:
            idx: the index of the child node (if `clazz` provided,
                 only consideres child nodes of requested type)
            clazz: the type to nodes to be considered, optional

        Returns:
            QueryNode: the child node of this node or ``None``
                       if not child was found (e.g. type mismatch or index out of bounds)
        """
        if not self.children or idx < 0 or idx > self.child_count:
            return None
        if not clazz:
            return self.children[idx]
        pos = 0
        for child in self.children:
            if isinstance(child, clazz):
                if pos == idx:
                    return child
                pos += 1
        return None

    def get_first_child(self, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get this first child node.

        Args:
            clazz: the type to nodes to be considered

        Returns:
            QueryNode: the first child node of this node or ``None``
        """
        return self.get_child(0, clazz=clazz)

    def get_last_child(self, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get this last child node.

        Args:
            clazz: the type to nodes to be considered

        Returns:
            QueryNode: the last child node of this node or ``None``
        """
        return self.get_child(self.child_count - 1, clazz=clazz)

    def __str__(self) -> str:
        chs = " ".join(map(str, self.children))
        strrepr = f"({self.node_type!s}{' ' + chs if chs else ''})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    @abstractmethod
    def accept(self, visitor: QueryVisitor) -> None:
        pass


# ---------------------------------------------------------------------------


class Modifier(QueryNode):
    """A LexCQL expression tree modifier node."""

    def __init__(self, name: str, relation: Optional[str], value: Optional[str]):
        """[Constructor]

        Args:
            name: the modifier name
            relation: the modifier relation symbol or ``None``
            value: the modifier relation value or ``None``
        """
        super().__init__(QueryNodeType.MODIFIER)

        self.name = name
        """the modifier name"""
        self.relation = relation
        """the modifier relation symbol"""
        self.value = value
        """the modifier relation value"""

    def __str__(self) -> str:
        parts = list()
        parts.append(f"({self.node_type!s} ")
        parts.append(f"/{self.name}")
        if self.relation:
            parts.append(f" {self.relation}")
            parts.append(f" {self.value}")
        parts.append(")")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


class Relation(QueryNode):
    """A LexCQL expression tree relation node."""

    def __init__(self, relation: str, modifiers: Optional[List[Modifier]] = None):
        """[Constructor]

        Args:
            relation: the relation name or symbol
            modifiers: the list of modifiers for this relation or ``None``
        """
        super().__init__(QueryNodeType.RELATION, children=modifiers)

        self.relation = relation
        """the relation"""

    def get_modifiers(self) -> List[Modifier]:
        """Get the modifiers.

        Returns:
            List[Modifier]: the modifiers
        """
        return self.children

    @property
    def modifiers(self) -> List[Modifier]:
        """the list of modifiers for this relation or ``None``"""
        return self.get_modifiers()

    def __str__(self):
        parts = list()
        parts.append(f"({self.node_type!s} {self.relation}")
        if self.modifiers:
            for modifier in self.modifiers:
                parts.append(f" {modifier!s}")
        parts.append(")")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


class SearchClause(QueryNode):
    """A LexCQL expression tree search_clause node."""

    def __init__(self, index: Optional[str], relation: Optional[Relation], search_term: str):
        """[Constructor]

        Args:
            index: the index (or field) or ``None``
            relation: the relation or ``None``
            search_term: the search term
        """
        super().__init__(QueryNodeType.SEARCH_CLAUSE, child=relation)

        self.index = index if (index is not None and index.strip()) else None
        """the index (or field) or ``None``"""
        self.search_term = search_term
        """the search term"""

    def get_relation(self) -> Optional[Relation]:
        """Get the relation.

        Returns:
            Optional[Relation]: the relation or ``None``
        """
        return self.get_child(0, Relation)

    @property
    def relation(self) -> Optional[Relation]:
        """the relation or ``None``"""
        return self.get_relation()

    def has_index_and_relation(self) -> bool:
        """Check if index and relation in this search clause are set.

        Returns:
            bool: ``True`` if index and relation were set, ``False`` otherwise
        """
        return self.index is not None and self.relation is not None

    def __str__(self):
        parts = list()
        parts.append(f"({self.node_type!s} ")
        if self.index is not None:
            parts.append(f"{self.index} ")
        if self.relation is not None:
            parts.append(f"{self.relation!s} ")
        parts.append(f"{self.search_term})")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


class SearchClauseGroup(QueryNode):
    """A LexCQL expression tree search_clausse_group node."""

    def __init__(self, leftChild: QueryNode, r_boolean: RBoolean, rightChild: QueryNode):
        """[Constructor]

        Args:
            leftChild: the left child (search clause or group).
            r_boolean: the boolean
            rightChild: the right child (search clause or group).
        """
        super().__init__(QueryNodeType.SEARCH_CLAUSE_GROUP, children=[leftChild, rightChild])

        self.r_boolean = r_boolean
        """the boolean"""

    def get_left_child(self) -> QueryNode:
        """Get the left child (search clause or group).

        Returns:
            QueryNode: the left child (search clause or group)
        """
        return self.children[0]

    def get_right_child(self) -> QueryNode:
        """Get the right child (search clause or group).

        Returns:
            QueryNode: the right child (search clause or group)
        """
        return self.children[1]

    def get_boolean(self) -> RBoolean:
        """Get the boolean.

        Returns:
            RBoolean: the boolean
        """
        return self.r_boolean

    @property
    def left_child(self) -> QueryNode:
        return self.get_left_child()

    @property
    def right_child(self) -> QueryNode:
        return self.get_right_child()

    @property
    def boolean(self) -> QueryNode:
        return self.get_boolean()

    def has_boolean(self, r_boolean: RBoolean) -> bool:
        """Check if expression used a given boolean.

        Args:
            r_boolean: the boolean to check

        Returns:
            bool: ``True`` if the given boolean was used, ``False`` otherwise

        Raises:
            TypeError: if r_boolean is ``None``
        """
        if r_boolean is None:
            raise TypeError("r_boolean is None")
        return self.r_boolean == r_boolean

    def __str__(self):
        parts = list()
        parts.append(f"({self.node_type!s} ")
        parts.append(f"{self.children[0]!s} {self.r_boolean!s} {self.children[1]!s}")
        parts.append(")")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


class Subquery(QueryNode):
    """A LexCQL expression tree search_clausse_group node."""

    def __init__(self, child: QueryNode, inParentheses: bool):
        """[Constructor]

        Args:
            child (QueryNode): the inner child.
            inParentheses: is this query node in parentheses.
        """
        super().__init__(QueryNodeType.SUBQUERY, child=child)

        self.inParentheses = inParentheses
        """Is this query node in parentheses."""

    def get_child(self) -> QueryNode:
        """Get the inner child

        Returns:
            QueryNode: the right child
        """
        return self.children[0]

    @property
    def child(self) -> QueryNode:
        return self.get_child()

    def is_in_parentheses(self) -> bool:
        """Is this query node in parentheses.

        Returns:
            bool: ``True`` if this query node is in parentheses, ``False`` otherwise
        """
        return self.inParentheses

    def __str__(self):
        parts = list()
        parts.append(f"({self.node_type!s} ")
        if self.inParentheses:
            parts.append('"(" ')
        parts.append(f"{self.children[0]!s}")
        if self.inParentheses:
            parts.append(' ")"')
        parts.append(")")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ErrorDetail:
    message: str
    type: Optional[Union[Literal["syntax-error", "validation-error"], str]] = None
    position: Optional[Union[int, SourceLocation]] = None
    fragment: Optional[str] = None


class ErrorListener(antlr4.error.ErrorListener.ErrorListener):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query
        self.errors: List[ErrorDetail] = list()

    def syntaxError(
        self, recognizer: Recognizer, offendingSymbol: Optional[Token], line: int, column: int, msg: str, e
    ):
        # FIXME: additional information of error should not be logged but added
        # to the list of errors; that list probably needs to be enhanced to
        # store supplementary information.
        # Furthermore, a sophisticated errorlist implementation could also be
        # used by the QueryVistor to add addition query error information.

        pos = None
        fragment = None
        if isinstance(offendingSymbol, Token):
            pos = offendingSymbol.start
            fragment = self.query[: pos + len(offendingSymbol.text)]

        if LOGGER.isEnabledFor(logging.DEBUG):
            if pos is not None and pos != -1:
                LOGGER.debug("query: %s", self.query)
                LOGGER.debug("       %s^- %s", " " * pos, msg)

            if isinstance(recognizer, LexParser):
                LOGGER.debug("symbol: %s", recognizer.symbolicNames[offendingSymbol.type])
                LOGGER.debug("literal: %s", recognizer.literalNames[offendingSymbol.type])
                LOGGER.debug("token idx: %s", offendingSymbol.tokenIndex)

        if pos is None:
            pos = column

        self.errors.append(
            ErrorDetail(
                message=msg,
                type="syntax-error",
                position=SourceLocation.fromToken(offendingSymbol) if isinstance(offendingSymbol, Token) else pos,
                fragment=fragment,
            )
        )

    def has_errors(self) -> bool:
        return bool(self.errors)


class QueryParserException(Exception):
    """Query parser exception."""


class ExpressionTreeBuilderException(Exception):
    """Error building expression tree."""


class ExpressionTreeBuilder(LexParserVisitor):
    def __init__(self, parser: "QueryParser") -> None:
        super().__init__()
        self.parser = parser
        self.stack: Deque[Any] = deque()

    # ----------------------------------------------------

    def visitQuery(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitQuery(ctx)

        LOGGER.debug("visitQuery/exit: stack=%s", self.stack)
        return None

    def visitBoolean_query(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitBoolean_query/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitBoolean_query(ctx)

        if len(self.stack) > pos:
            if len(self.stack) - pos == 1:
                # TODO: noop?
                node: QueryNode = self.stack.pop()
                self.stack.append(node)
            else:
                children: List[QueryNode] = []
                while len(self.stack) > pos:
                    children.insert(0, self.stack.pop())

                # build tree
                node: QueryNode = children.pop(0)
                while len(children) >= 2:
                    rBoolean: RBoolean = children.pop(0)
                    other: QueryNode = children.pop(0)
                    node = SearchClauseGroup(node, rBoolean, other)
                    if self.parser.enableSourceLocations:
                        node.location = SourceLocation.fromContext(ctx)

                if len(children) > 0:
                    raise ExpressionTreeBuilderException(
                        "visitBoolean_query children length does not match into tree structure!"
                    )

                # "return" the tree
                self.stack.append(node)
        else:
            raise ExpressionTreeBuilderException("visitBoolean_query is empty")

        LOGGER.debug("visitBoolean_query/exit: stack=%s", self.stack)
        return None

    def visitSubquery(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitSubquery/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitSubquery(ctx)

        if ctx.boolean_query() is not None:
            node: QueryNode = self.stack.pop()
            sqNode = Subquery(node, inParentheses=True)
            if self.parser.enableSourceLocations:
                sqNode.location = SourceLocation.fromContext(ctx)
            self.stack.append(sqNode)
        elif ctx.search_clause() is not None:
            # TODO: noop?
            searchClause: SearchClause = self.stack.pop()
            self.stack.append(searchClause)

        LOGGER.debug("visitSubquery/exit: stack=%s", self.stack)
        return None

    def visitBoolean_modified(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitBoolean_modified/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        b_ctx = ctx.r_boolean()
        if b_ctx.AND() is not None:
            self.stack.append(RBoolean.AND)
        elif b_ctx.OR() is not None:
            self.stack.append(RBoolean.OR)
        elif b_ctx.NOT() is not None:
            self.stack.append(RBoolean.NOT)
        else:
            raise ExpressionTreeBuilderException(f"invalid boolean for boolean_modified: {b_ctx.getText()}")

        if ctx.modifier_list() is not None:
            raise ExpressionTreeBuilderException(
                f"boolean_modified does not support modifiers on booleans in LexCQL: {ctx.modifier_list().getText()}"
            )

        LOGGER.debug("visitBoolean_modified/exit: stack=%s", self.stack)
        return None

    def visitSearch_clause(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitSearch_clause/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitSearch_clause(ctx)

        searchTerm: str = self.stack.pop()
        relation: Optional[Relation] = None
        index: Optional[str] = None
        if ctx.index() is not None:
            relation = self.stack.pop()
            index = self.stack.pop()

        node = SearchClause(index, relation, searchTerm)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitSearch_clause/exit: stack=%s", self.stack)
        return None

    def visitSearch_term(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitSearch_term/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        searchTerm: str
        if ctx.SIMPLE_STRING() is not None:
            tn: TerminalNodeImpl = ctx.SIMPLE_STRING()
            assert isinstance(tn, TerminalNodeImpl), "visitSearch_term ctx.SIMPLE_STRING() must be TerminalNodeImpl"
            searchTerm = tn.getSymbol().text
        elif ctx.QUOTED_STRING() is not None:
            tn: TerminalNodeImpl = ctx.QUOTED_STRING()
            assert isinstance(tn, TerminalNodeImpl), "visitSearch_term ctx.QUOTED_STRING() must be TerminalNodeImpl"
            searchTerm = tn.getSymbol().text
            searchTerm = self.unquoteString(searchTerm)
        else:
            raise ExpressionTreeBuilderException("Invalid state in visitSearch_term! No string?")

        self.stack.append(searchTerm)

        LOGGER.debug("visitSearch_term/exit: stack=%s", self.stack)
        return None

    def visitIndex(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitIndex/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        child = ctx.getChild(0)
        assert hasattr(child, "getText"), "ctx.getChild(0) must have getText() method"
        name: str = child.getText()
        self.stack.append(name)

        LOGGER.debug("visitIndex/exit: stack=%s", self.stack)
        return None

    def visitRelation_modified(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitRelation_modified/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitRelation_modified(ctx)

        m_ctx = ctx.modifier_list()
        modifiers: List[Modifier] = []
        if m_ctx is not None:
            modifiers: List[Modifier] = self.stack.pop()

        name: str = self.stack.pop()

        node = Relation(name, modifiers)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitRelation_modified/exit: stack=%s", self.stack)
        return None

    def visitRelation(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitRelation/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        # TODO: validate supported relations only?
        relation = ctx.getText()
        self.stack.append(relation)

        LOGGER.debug("visitRelation/exit: stack=%s", self.stack)
        return None

    def visitModifier_list(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitModifier_list/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitModifier_list(ctx)

        if len(self.stack) > pos:
            modifiers: List[Modifier] = []
            while len(self.stack) > pos:
                modifiers.insert(0, self.stack.pop())
            self.stack.append(modifiers)
        else:
            raise ExpressionTreeBuilderException("visitModifier_list is empty!")

        LOGGER.debug("visitModifier_list/exit: stack=%s", self.stack)
        return None

    def visitModifier(self, ctx):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitModifier/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        tn: TerminalNodeImpl = ctx.modifier_name().simple_name().SIMPLE_STRING()
        assert isinstance(
            tn, TerminalNodeImpl
        ), "visitModifier ctx.modifier_name().simple_name().SIMPLE_STRING() must be TerminalNodeImpl"
        name: str = tn.getSymbol().text
        relation: Optional[str] = None
        value: Optional[str] = None

        r_ctx = ctx.modifier_relation()
        if r_ctx is not None:
            relation = r_ctx.relation_symbol().getText()
            tn: TerminalNodeImpl = r_ctx.modifier_value().SIMPLE_STRING()
            assert isinstance(
                tn, TerminalNodeImpl
            ), "visitModifier r_ctx.modifier_value().SIMPLE_STRING() must be TerminalNodeImpl"
            value = tn.getSymbol().text

        node = Modifier(name, relation, value)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitModifier/exit: stack=%s", self.stack)

    # ----------------------------------------------------

    @staticmethod
    def unquoteString(value: str):
        # strip quotes
        if value.startswith('"'):
            if value.endswith('"'):
                value = value[1:-1]
            else:
                raise ExpressionTreeBuilderException("value not properly quoted; invalid closing quote")
        else:
            raise ExpressionTreeBuilderException('value not properly quoted; expected " (double quote) character')

        # unescape characters
        chars = list()
        i = 0
        while i < len(value):
            ch = value[i]
            if ch == "\\":
                i += 1
                ch = value[i]

                if value == "\\":  # slash
                    chars.append("\\")
                elif value == '"':  # double quote
                    chars.append('"')
                else:
                    raise ExpressionTreeBuilderException(f"invalid escape sequence: {ch}")

            else:
                chars.append(ch)

            i += 1

        return "".join(chars)


class QueryParser:
    """A LexCQL query parser that produces LexCQL expression trees."""

    def __init__(self, enableSourceLocations: bool = False):
        """[Constructor]

        Args:
            enableSourceLocations: whether source locations are computed for each query node. Defaults to False.
        """
        self.enableSourceLocations = enableSourceLocations
        """Whether source locations are computed for each query node."""

        self.errors: List[ErrorDetail] = list()
        """List of errors when parsing fails."""

    def parse(self, query: str) -> QueryNode:
        """Parse query.

        Args:
            query: the raw LexCQL query

        Raises:
            QueryParserException: if an error occurred

        Returns:
            QueryNode: a LexCQL expression tree
        """
        error_listener = ErrorListener(query)
        try:
            input_stream = InputStream(query)
            lexer = LexLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = LexParser(stream)

            # clear (possible) default error listeners and set our own!
            lexer.removeErrorListeners()
            parser.removeErrorListeners()
            lexer.addErrorListener(error_listener)
            parser.addErrorListener(error_listener)
            # ExceptionThrowingErrorListener ?

            # commence parsing ...
            tree: LexParser.QueryContext = parser.query()

            if not error_listener.has_errors() and parser.getNumberOfSyntaxErrors() == 0:
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug("ANTLR parse tree: %s", tree.toStringTree(LexParser.ruleNames))

                # now build the expression tree
                builder = ExpressionTreeBuilder(self)
                builder.visit(tree)
                node: QueryNode = builder.stack.pop()
                return node
            else:
                if LOGGER.isEnabledFor(logging.DEBUG):
                    for msg in error_listener.errors:
                        LOGGER.debug("ERROR: %s", msg)

                raise QueryParserException("unable to parse query")
        except ExpressionTreeBuilderException as ex:
            raise QueryParserException(str(ex)) from ex
        except QueryParserException:
            raise
        except Exception as ex:
            raise QueryParserException("an unexpected exception occured while parsing") from ex
        finally:
            # update list of errors
            self.errors = error_listener.errors


# ---------------------------------------------------------------------------
