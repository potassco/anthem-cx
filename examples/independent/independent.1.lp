{ in(X) } :- node(X).
:- in(X), in(Y), edge(X,Y).
blocked(X) :- in(Y), edge(X,Y).
:- node(X), not in(X), not blocked(X).
