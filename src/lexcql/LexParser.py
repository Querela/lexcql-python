# Generated from LexParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,17,118,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        1,0,1,0,1,1,1,1,1,1,1,1,5,1,48,8,1,10,1,12,1,51,9,1,1,2,1,2,1,2,
        1,2,1,2,3,2,58,8,2,1,3,1,3,1,3,3,3,63,8,3,1,3,1,3,1,4,1,4,1,5,1,
        5,3,5,71,8,5,1,6,1,6,3,6,75,8,6,1,7,1,7,3,7,79,8,7,1,8,1,8,3,8,83,
        8,8,1,9,1,9,1,10,1,10,3,10,89,8,10,1,11,1,11,1,12,4,12,94,8,12,11,
        12,12,12,95,1,13,1,13,1,13,3,13,101,8,13,1,14,1,14,1,15,1,15,1,15,
        1,16,1,16,1,17,1,17,1,17,1,17,1,18,1,18,1,19,1,19,1,19,0,0,20,0,
        2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,0,3,1,0,15,
        16,1,0,3,9,1,0,11,13,107,0,40,1,0,0,0,2,43,1,0,0,0,4,57,1,0,0,0,
        6,62,1,0,0,0,8,66,1,0,0,0,10,70,1,0,0,0,12,72,1,0,0,0,14,78,1,0,
        0,0,16,82,1,0,0,0,18,84,1,0,0,0,20,86,1,0,0,0,22,90,1,0,0,0,24,93,
        1,0,0,0,26,97,1,0,0,0,28,102,1,0,0,0,30,104,1,0,0,0,32,107,1,0,0,
        0,34,109,1,0,0,0,36,113,1,0,0,0,38,115,1,0,0,0,40,41,3,2,1,0,41,
        42,5,0,0,1,42,1,1,0,0,0,43,49,3,4,2,0,44,45,3,20,10,0,45,46,3,4,
        2,0,46,48,1,0,0,0,47,44,1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,0,49,50,
        1,0,0,0,50,3,1,0,0,0,51,49,1,0,0,0,52,53,5,1,0,0,53,54,3,2,1,0,54,
        55,5,2,0,0,55,58,1,0,0,0,56,58,3,6,3,0,57,52,1,0,0,0,57,56,1,0,0,
        0,58,5,1,0,0,0,59,60,3,10,5,0,60,61,3,12,6,0,61,63,1,0,0,0,62,59,
        1,0,0,0,62,63,1,0,0,0,63,64,1,0,0,0,64,65,3,8,4,0,65,7,1,0,0,0,66,
        67,7,0,0,0,67,9,1,0,0,0,68,71,3,38,19,0,69,71,3,34,17,0,70,68,1,
        0,0,0,70,69,1,0,0,0,71,11,1,0,0,0,72,74,3,14,7,0,73,75,3,24,12,0,
        74,73,1,0,0,0,74,75,1,0,0,0,75,13,1,0,0,0,76,79,3,16,8,0,77,79,3,
        18,9,0,78,76,1,0,0,0,78,77,1,0,0,0,79,15,1,0,0,0,80,83,3,38,19,0,
        81,83,3,34,17,0,82,80,1,0,0,0,82,81,1,0,0,0,83,17,1,0,0,0,84,85,
        7,1,0,0,85,19,1,0,0,0,86,88,3,22,11,0,87,89,3,24,12,0,88,87,1,0,
        0,0,88,89,1,0,0,0,89,21,1,0,0,0,90,91,7,2,0,0,91,23,1,0,0,0,92,94,
        3,26,13,0,93,92,1,0,0,0,94,95,1,0,0,0,95,93,1,0,0,0,95,96,1,0,0,
        0,96,25,1,0,0,0,97,98,5,10,0,0,98,100,3,28,14,0,99,101,3,30,15,0,
        100,99,1,0,0,0,100,101,1,0,0,0,101,27,1,0,0,0,102,103,3,38,19,0,
        103,29,1,0,0,0,104,105,3,18,9,0,105,106,3,32,16,0,106,31,1,0,0,0,
        107,108,7,0,0,0,108,33,1,0,0,0,109,110,3,36,18,0,110,111,5,14,0,
        0,111,112,3,38,19,0,112,35,1,0,0,0,113,114,3,38,19,0,114,37,1,0,
        0,0,115,116,5,16,0,0,116,39,1,0,0,0,10,49,57,62,70,74,78,82,88,95,
        100
    ]

class LexParser ( Parser ):

    grammarFileName = "LexParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'='", "'>'", "'<'", "'>='", 
                     "'<='", "'<>'", "'=='", "'/'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'.'" ]

    symbolicNames = [ "<INVALID>", "L_PAREN", "R_PAREN", "EQUAL", "GREATER", 
                      "LESSER", "GREATER_EQUAL", "LESSER_EQUAL", "NOT_EQUAL", 
                      "EQUAL_EQUAL", "SLASH", "AND", "OR", "NOT", "DOT", 
                      "QUOTED_STRING", "SIMPLE_STRING", "WS" ]

    RULE_query = 0
    RULE_boolean_query = 1
    RULE_subquery = 2
    RULE_search_clause = 3
    RULE_search_term = 4
    RULE_index = 5
    RULE_relation_modified = 6
    RULE_relation = 7
    RULE_relation_name = 8
    RULE_relation_symbol = 9
    RULE_boolean_modified = 10
    RULE_r_boolean = 11
    RULE_modifier_list = 12
    RULE_modifier = 13
    RULE_modifier_name = 14
    RULE_modifier_relation = 15
    RULE_modifier_value = 16
    RULE_prefix_name = 17
    RULE_prefix = 18
    RULE_simple_name = 19

    ruleNames =  [ "query", "boolean_query", "subquery", "search_clause", 
                   "search_term", "index", "relation_modified", "relation", 
                   "relation_name", "relation_symbol", "boolean_modified", 
                   "r_boolean", "modifier_list", "modifier", "modifier_name", 
                   "modifier_relation", "modifier_value", "prefix_name", 
                   "prefix", "simple_name" ]

    EOF = Token.EOF
    L_PAREN=1
    R_PAREN=2
    EQUAL=3
    GREATER=4
    LESSER=5
    GREATER_EQUAL=6
    LESSER_EQUAL=7
    NOT_EQUAL=8
    EQUAL_EQUAL=9
    SLASH=10
    AND=11
    OR=12
    NOT=13
    DOT=14
    QUOTED_STRING=15
    SIMPLE_STRING=16
    WS=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolean_query(self):
            return self.getTypedRuleContext(LexParser.Boolean_queryContext,0)


        def EOF(self):
            return self.getToken(LexParser.EOF, 0)

        def getRuleIndex(self):
            return LexParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)




    def query(self):

        localctx = LexParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_query)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.boolean_query()
            self.state = 41
            self.match(LexParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Boolean_queryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subquery(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LexParser.SubqueryContext)
            else:
                return self.getTypedRuleContext(LexParser.SubqueryContext,i)


        def boolean_modified(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LexParser.Boolean_modifiedContext)
            else:
                return self.getTypedRuleContext(LexParser.Boolean_modifiedContext,i)


        def getRuleIndex(self):
            return LexParser.RULE_boolean_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean_query" ):
                listener.enterBoolean_query(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean_query" ):
                listener.exitBoolean_query(self)




    def boolean_query(self):

        localctx = LexParser.Boolean_queryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_boolean_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.subquery()
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0):
                self.state = 44
                self.boolean_modified()
                self.state = 45
                self.subquery()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubqueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_PAREN(self):
            return self.getToken(LexParser.L_PAREN, 0)

        def boolean_query(self):
            return self.getTypedRuleContext(LexParser.Boolean_queryContext,0)


        def R_PAREN(self):
            return self.getToken(LexParser.R_PAREN, 0)

        def search_clause(self):
            return self.getTypedRuleContext(LexParser.Search_clauseContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_subquery

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubquery" ):
                listener.enterSubquery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubquery" ):
                listener.exitSubquery(self)




    def subquery(self):

        localctx = LexParser.SubqueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_subquery)
        try:
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                self.match(LexParser.L_PAREN)
                self.state = 53
                self.boolean_query()
                self.state = 54
                self.match(LexParser.R_PAREN)
                pass
            elif token in [15, 16]:
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.search_clause()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Search_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def search_term(self):
            return self.getTypedRuleContext(LexParser.Search_termContext,0)


        def index(self):
            return self.getTypedRuleContext(LexParser.IndexContext,0)


        def relation_modified(self):
            return self.getTypedRuleContext(LexParser.Relation_modifiedContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_search_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSearch_clause" ):
                listener.enterSearch_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSearch_clause" ):
                listener.exitSearch_clause(self)




    def search_clause(self):

        localctx = LexParser.Search_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_search_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 59
                self.index()
                self.state = 60
                self.relation_modified()


            self.state = 64
            self.search_term()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Search_termContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIMPLE_STRING(self):
            return self.getToken(LexParser.SIMPLE_STRING, 0)

        def QUOTED_STRING(self):
            return self.getToken(LexParser.QUOTED_STRING, 0)

        def getRuleIndex(self):
            return LexParser.RULE_search_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSearch_term" ):
                listener.enterSearch_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSearch_term" ):
                listener.exitSearch_term(self)




    def search_term(self):

        localctx = LexParser.Search_termContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_search_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IndexContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_name(self):
            return self.getTypedRuleContext(LexParser.Simple_nameContext,0)


        def prefix_name(self):
            return self.getTypedRuleContext(LexParser.Prefix_nameContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_index

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndex" ):
                listener.enterIndex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndex" ):
                listener.exitIndex(self)




    def index(self):

        localctx = LexParser.IndexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_index)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.simple_name()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.prefix_name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Relation_modifiedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relation(self):
            return self.getTypedRuleContext(LexParser.RelationContext,0)


        def modifier_list(self):
            return self.getTypedRuleContext(LexParser.Modifier_listContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_relation_modified

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation_modified" ):
                listener.enterRelation_modified(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation_modified" ):
                listener.exitRelation_modified(self)




    def relation_modified(self):

        localctx = LexParser.Relation_modifiedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_relation_modified)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.relation()
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 73
                self.modifier_list()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relation_name(self):
            return self.getTypedRuleContext(LexParser.Relation_nameContext,0)


        def relation_symbol(self):
            return self.getTypedRuleContext(LexParser.Relation_symbolContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation" ):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation" ):
                listener.exitRelation(self)




    def relation(self):

        localctx = LexParser.RelationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_relation)
        try:
            self.state = 78
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.relation_name()
                pass
            elif token in [3, 4, 5, 6, 7, 8, 9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.relation_symbol()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Relation_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_name(self):
            return self.getTypedRuleContext(LexParser.Simple_nameContext,0)


        def prefix_name(self):
            return self.getTypedRuleContext(LexParser.Prefix_nameContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_relation_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation_name" ):
                listener.enterRelation_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation_name" ):
                listener.exitRelation_name(self)




    def relation_name(self):

        localctx = LexParser.Relation_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_relation_name)
        try:
            self.state = 82
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.simple_name()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 81
                self.prefix_name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Relation_symbolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUAL(self):
            return self.getToken(LexParser.EQUAL, 0)

        def GREATER(self):
            return self.getToken(LexParser.GREATER, 0)

        def LESSER(self):
            return self.getToken(LexParser.LESSER, 0)

        def GREATER_EQUAL(self):
            return self.getToken(LexParser.GREATER_EQUAL, 0)

        def LESSER_EQUAL(self):
            return self.getToken(LexParser.LESSER_EQUAL, 0)

        def NOT_EQUAL(self):
            return self.getToken(LexParser.NOT_EQUAL, 0)

        def EQUAL_EQUAL(self):
            return self.getToken(LexParser.EQUAL_EQUAL, 0)

        def getRuleIndex(self):
            return LexParser.RULE_relation_symbol

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation_symbol" ):
                listener.enterRelation_symbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation_symbol" ):
                listener.exitRelation_symbol(self)




    def relation_symbol(self):

        localctx = LexParser.Relation_symbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_relation_symbol)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1016) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Boolean_modifiedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def r_boolean(self):
            return self.getTypedRuleContext(LexParser.R_booleanContext,0)


        def modifier_list(self):
            return self.getTypedRuleContext(LexParser.Modifier_listContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_boolean_modified

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean_modified" ):
                listener.enterBoolean_modified(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean_modified" ):
                listener.exitBoolean_modified(self)




    def boolean_modified(self):

        localctx = LexParser.Boolean_modifiedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_boolean_modified)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.r_boolean()
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 87
                self.modifier_list()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class R_booleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(LexParser.AND, 0)

        def OR(self):
            return self.getToken(LexParser.OR, 0)

        def NOT(self):
            return self.getToken(LexParser.NOT, 0)

        def getRuleIndex(self):
            return LexParser.RULE_r_boolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterR_boolean" ):
                listener.enterR_boolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitR_boolean" ):
                listener.exitR_boolean(self)




    def r_boolean(self):

        localctx = LexParser.R_booleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_r_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Modifier_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def modifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LexParser.ModifierContext)
            else:
                return self.getTypedRuleContext(LexParser.ModifierContext,i)


        def getRuleIndex(self):
            return LexParser.RULE_modifier_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier_list" ):
                listener.enterModifier_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier_list" ):
                listener.exitModifier_list(self)




    def modifier_list(self):

        localctx = LexParser.Modifier_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_modifier_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 92
                self.modifier()
                self.state = 95 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==10):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self):
            return self.getToken(LexParser.SLASH, 0)

        def modifier_name(self):
            return self.getTypedRuleContext(LexParser.Modifier_nameContext,0)


        def modifier_relation(self):
            return self.getTypedRuleContext(LexParser.Modifier_relationContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_modifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier" ):
                listener.enterModifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier" ):
                listener.exitModifier(self)




    def modifier(self):

        localctx = LexParser.ModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_modifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(LexParser.SLASH)
            self.state = 98
            self.modifier_name()
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1016) != 0):
                self.state = 99
                self.modifier_relation()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Modifier_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_name(self):
            return self.getTypedRuleContext(LexParser.Simple_nameContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_modifier_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier_name" ):
                listener.enterModifier_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier_name" ):
                listener.exitModifier_name(self)




    def modifier_name(self):

        localctx = LexParser.Modifier_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_modifier_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.simple_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Modifier_relationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relation_symbol(self):
            return self.getTypedRuleContext(LexParser.Relation_symbolContext,0)


        def modifier_value(self):
            return self.getTypedRuleContext(LexParser.Modifier_valueContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_modifier_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier_relation" ):
                listener.enterModifier_relation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier_relation" ):
                listener.exitModifier_relation(self)




    def modifier_relation(self):

        localctx = LexParser.Modifier_relationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_modifier_relation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.relation_symbol()
            self.state = 105
            self.modifier_value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Modifier_valueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIMPLE_STRING(self):
            return self.getToken(LexParser.SIMPLE_STRING, 0)

        def QUOTED_STRING(self):
            return self.getToken(LexParser.QUOTED_STRING, 0)

        def getRuleIndex(self):
            return LexParser.RULE_modifier_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier_value" ):
                listener.enterModifier_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier_value" ):
                listener.exitModifier_value(self)




    def modifier_value(self):

        localctx = LexParser.Modifier_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_modifier_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Prefix_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def prefix(self):
            return self.getTypedRuleContext(LexParser.PrefixContext,0)


        def DOT(self):
            return self.getToken(LexParser.DOT, 0)

        def simple_name(self):
            return self.getTypedRuleContext(LexParser.Simple_nameContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_prefix_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefix_name" ):
                listener.enterPrefix_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefix_name" ):
                listener.exitPrefix_name(self)




    def prefix_name(self):

        localctx = LexParser.Prefix_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_prefix_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.prefix()
            self.state = 110
            self.match(LexParser.DOT)
            self.state = 111
            self.simple_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrefixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_name(self):
            return self.getTypedRuleContext(LexParser.Simple_nameContext,0)


        def getRuleIndex(self):
            return LexParser.RULE_prefix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefix" ):
                listener.enterPrefix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefix" ):
                listener.exitPrefix(self)




    def prefix(self):

        localctx = LexParser.PrefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_prefix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.simple_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIMPLE_STRING(self):
            return self.getToken(LexParser.SIMPLE_STRING, 0)

        def getRuleIndex(self):
            return LexParser.RULE_simple_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_name" ):
                listener.enterSimple_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_name" ):
                listener.exitSimple_name(self)




    def simple_name(self):

        localctx = LexParser.Simple_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_simple_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(LexParser.SIMPLE_STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





