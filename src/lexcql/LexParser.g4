parser grammar LexParser;
options {
	tokenVocab = LexLexer;
}

/* ABNF: https://docs.oasis-open.org/search-ws/searchRetrieve/v1.0/os/part5-cql/searchRetrieve-v1.0-os-part5-cql.html */
/* Test in: http://lab.antlr.org/ */
/* Slides: https://www.esa.informatik.tu-darmstadt.de/archive/twiki/pub/Lectures/Compiler113De/antlr-v4-handout.pdf */

/* search clauses */

//  ! original ABNF rule: does not work due to left-recursion
//
//  query: search_clause_group;
//  search_clause_group: (search_clause_group boolean_modified subquery) | subquery;
//  subquery: (L_PAREN query R_PAREN) | search_clause;

//  flat lists as alternative? need to be interpreted left to right
//
//  search_clause_group: (subquery boolean_modified)* subquery;
//  search_clause_group: subquery (boolean_modified subquery)*;

// simplify and make it flat
query: boolean_query EOF;

boolean_query: subquery (boolean_modified subquery)*;

subquery: L_PAREN boolean_query R_PAREN | search_clause;

search_clause: (index relation_modified)? search_term;

search_term: SIMPLE_STRING | QUOTED_STRING;

/* indexes */

index: simple_name | prefix_name;

/* relations */

relation_modified: relation modifier_list?;

relation: relation_name | relation_symbol;

relation_name: simple_name | prefix_name;

relation_symbol:
	EQUAL
	| GREATER
	| LESSER
	| GREATER_EQUAL
	| LESSER_EQUAL
	| NOT_EQUAL
	| EQUAL_EQUAL;

/* booleans */

boolean_modified: r_boolean modifier_list?;

r_boolean: AND | OR | NOT;

/* modifiers */

modifier_list: modifier+;

modifier: SLASH modifier_name modifier_relation?;

modifier_name: simple_name;

modifier_relation: relation_symbol modifier_value;

modifier_value: SIMPLE_STRING | QUOTED_STRING;

/* terminal aliases */

prefix_name: prefix DOT simple_name;

prefix: simple_name;

simple_name: SIMPLE_STRING;