lexer grammar LexLexer;

/* search clauses */

L_PAREN: '(';
R_PAREN: ')';

/* relations */

EQUAL: '=';
GREATER: '>';
LESSER: '<';
GREATER_EQUAL: '>=';
LESSER_EQUAL: '<=';
NOT_EQUAL: '<>';
EQUAL_EQUAL: '==';

/* modifiers */

SLASH: '/';

/* booleans */

AND: [Aa][Nn][Dd];
OR: [Oo][Rr];
NOT: [Nn][Oo][Tt];

/* terminals */

DOT: '.';

QUOTED_STRING: '"' ('\\' ["\\] | ~["\\])* '"';

// whitespace must be explicit here as inverted sets can use rules/fragments
SIMPLE_STRING: (~["\\()/<=> \t\n\r])+;

/* whitespace */

WS: [ \t\n\r] -> channel(HIDDEN);