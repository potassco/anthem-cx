mark(X) :- goal(X).
:- not mark(X), start(X).
mark(Y) :- mark(X), path(Y,X).
{ path(Y,X) : edge(Y,X) } = 1 :- mark(X), not start(X).
