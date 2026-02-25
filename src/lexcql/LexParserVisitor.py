# Generated from LexParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LexParser import LexParser
else:
    from LexParser import LexParser

# This class defines a complete generic visitor for a parse tree produced by LexParser.

class LexParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LexParser#query.
    def visitQuery(self, ctx:LexParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#boolean_query.
    def visitBoolean_query(self, ctx:LexParser.Boolean_queryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#subquery.
    def visitSubquery(self, ctx:LexParser.SubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#search_clause.
    def visitSearch_clause(self, ctx:LexParser.Search_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#search_term.
    def visitSearch_term(self, ctx:LexParser.Search_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#index.
    def visitIndex(self, ctx:LexParser.IndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#relation_modified.
    def visitRelation_modified(self, ctx:LexParser.Relation_modifiedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#relation.
    def visitRelation(self, ctx:LexParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#relation_name.
    def visitRelation_name(self, ctx:LexParser.Relation_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#relation_symbol.
    def visitRelation_symbol(self, ctx:LexParser.Relation_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#boolean_modified.
    def visitBoolean_modified(self, ctx:LexParser.Boolean_modifiedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#r_boolean.
    def visitR_boolean(self, ctx:LexParser.R_booleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#modifier_list.
    def visitModifier_list(self, ctx:LexParser.Modifier_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#modifier.
    def visitModifier(self, ctx:LexParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#modifier_name.
    def visitModifier_name(self, ctx:LexParser.Modifier_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#modifier_relation.
    def visitModifier_relation(self, ctx:LexParser.Modifier_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#modifier_value.
    def visitModifier_value(self, ctx:LexParser.Modifier_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#prefix_name.
    def visitPrefix_name(self, ctx:LexParser.Prefix_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#prefix.
    def visitPrefix(self, ctx:LexParser.PrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LexParser#simple_name.
    def visitSimple_name(self, ctx:LexParser.Simple_nameContext):
        return self.visitChildren(ctx)



del LexParser