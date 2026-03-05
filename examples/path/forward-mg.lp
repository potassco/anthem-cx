visit(X) :- start(X).
:- not visit(X), goal(X).
visit(Y) :- visit(X), path(X,Y).
:- path(X,Y), path(X,Z), Y != Z.
{ path(X,Y) } :- visit(X), edge(X,Y), not goal(X).
