# Generated from LexParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LexParser import LexParser
else:
    from LexParser import LexParser

# This class defines a complete listener for a parse tree produced by LexParser.
class LexParserListener(ParseTreeListener):

    # Enter a parse tree produced by LexParser#query.
    def enterQuery(self, ctx:LexParser.QueryContext):
        pass

    # Exit a parse tree produced by LexParser#query.
    def exitQuery(self, ctx:LexParser.QueryContext):
        pass


    # Enter a parse tree produced by LexParser#boolean_query.
    def enterBoolean_query(self, ctx:LexParser.Boolean_queryContext):
        pass

    # Exit a parse tree produced by LexParser#boolean_query.
    def exitBoolean_query(self, ctx:LexParser.Boolean_queryContext):
        pass


    # Enter a parse tree produced by LexParser#subquery.
    def enterSubquery(self, ctx:LexParser.SubqueryContext):
        pass

    # Exit a parse tree produced by LexParser#subquery.
    def exitSubquery(self, ctx:LexParser.SubqueryContext):
        pass


    # Enter a parse tree produced by LexParser#search_clause.
    def enterSearch_clause(self, ctx:LexParser.Search_clauseContext):
        pass

    # Exit a parse tree produced by LexParser#search_clause.
    def exitSearch_clause(self, ctx:LexParser.Search_clauseContext):
        pass


    # Enter a parse tree produced by LexParser#search_term.
    def enterSearch_term(self, ctx:LexParser.Search_termContext):
        pass

    # Exit a parse tree produced by LexParser#search_term.
    def exitSearch_term(self, ctx:LexParser.Search_termContext):
        pass


    # Enter a parse tree produced by LexParser#index.
    def enterIndex(self, ctx:LexParser.IndexContext):
        pass

    # Exit a parse tree produced by LexParser#index.
    def exitIndex(self, ctx:LexParser.IndexContext):
        pass


    # Enter a parse tree produced by LexParser#relation_modified.
    def enterRelation_modified(self, ctx:LexParser.Relation_modifiedContext):
        pass

    # Exit a parse tree produced by LexParser#relation_modified.
    def exitRelation_modified(self, ctx:LexParser.Relation_modifiedContext):
        pass


    # Enter a parse tree produced by LexParser#relation.
    def enterRelation(self, ctx:LexParser.RelationContext):
        pass

    # Exit a parse tree produced by LexParser#relation.
    def exitRelation(self, ctx:LexParser.RelationContext):
        pass


    # Enter a parse tree produced by LexParser#relation_name.
    def enterRelation_name(self, ctx:LexParser.Relation_nameContext):
        pass

    # Exit a parse tree produced by LexParser#relation_name.
    def exitRelation_name(self, ctx:LexParser.Relation_nameContext):
        pass


    # Enter a parse tree produced by LexParser#relation_symbol.
    def enterRelation_symbol(self, ctx:LexParser.Relation_symbolContext):
        pass

    # Exit a parse tree produced by LexParser#relation_symbol.
    def exitRelation_symbol(self, ctx:LexParser.Relation_symbolContext):
        pass


    # Enter a parse tree produced by LexParser#boolean_modified.
    def enterBoolean_modified(self, ctx:LexParser.Boolean_modifiedContext):
        pass

    # Exit a parse tree produced by LexParser#boolean_modified.
    def exitBoolean_modified(self, ctx:LexParser.Boolean_modifiedContext):
        pass


    # Enter a parse tree produced by LexParser#r_boolean.
    def enterR_boolean(self, ctx:LexParser.R_booleanContext):
        pass

    # Exit a parse tree produced by LexParser#r_boolean.
    def exitR_boolean(self, ctx:LexParser.R_booleanContext):
        pass


    # Enter a parse tree produced by LexParser#modifier_list.
    def enterModifier_list(self, ctx:LexParser.Modifier_listContext):
        pass

    # Exit a parse tree produced by LexParser#modifier_list.
    def exitModifier_list(self, ctx:LexParser.Modifier_listContext):
        pass


    # Enter a parse tree produced by LexParser#modifier.
    def enterModifier(self, ctx:LexParser.ModifierContext):
        pass

    # Exit a parse tree produced by LexParser#modifier.
    def exitModifier(self, ctx:LexParser.ModifierContext):
        pass


    # Enter a parse tree produced by LexParser#modifier_name.
    def enterModifier_name(self, ctx:LexParser.Modifier_nameContext):
        pass

    # Exit a parse tree produced by LexParser#modifier_name.
    def exitModifier_name(self, ctx:LexParser.Modifier_nameContext):
        pass


    # Enter a parse tree produced by LexParser#modifier_relation.
    def enterModifier_relation(self, ctx:LexParser.Modifier_relationContext):
        pass

    # Exit a parse tree produced by LexParser#modifier_relation.
    def exitModifier_relation(self, ctx:LexParser.Modifier_relationContext):
        pass


    # Enter a parse tree produced by LexParser#modifier_value.
    def enterModifier_value(self, ctx:LexParser.Modifier_valueContext):
        pass

    # Exit a parse tree produced by LexParser#modifier_value.
    def exitModifier_value(self, ctx:LexParser.Modifier_valueContext):
        pass


    # Enter a parse tree produced by LexParser#prefix_name.
    def enterPrefix_name(self, ctx:LexParser.Prefix_nameContext):
        pass

    # Exit a parse tree produced by LexParser#prefix_name.
    def exitPrefix_name(self, ctx:LexParser.Prefix_nameContext):
        pass


    # Enter a parse tree produced by LexParser#prefix.
    def enterPrefix(self, ctx:LexParser.PrefixContext):
        pass

    # Exit a parse tree produced by LexParser#prefix.
    def exitPrefix(self, ctx:LexParser.PrefixContext):
        pass


    # Enter a parse tree produced by LexParser#simple_name.
    def enterSimple_name(self, ctx:LexParser.Simple_nameContext):
        pass

    # Exit a parse tree produced by LexParser#simple_name.
    def exitSimple_name(self, ctx:LexParser.Simple_nameContext):
        pass



del LexParser