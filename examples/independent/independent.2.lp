{ in(X) } :- node(X).
:- in(X), in(Y), edge(X,Y).
neighbor_in(X) :- in(Y), edge(Y,X).
:- node(X), not in(X), not neighbor_in(X).
