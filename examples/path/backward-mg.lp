mark(X) :- goal(X).
:- not mark(X), start(X).
mark(Y) :- mark(X), path(Y,X).
:- path(Y,X), path(Z,X), Y != Z.
{ path(Y,X) } :- mark(X), edge(Y,X), not start(X).
