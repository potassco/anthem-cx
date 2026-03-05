visit(X) :- start(X).
:- not visit(X), goal(X).
visit(Y) :- visit(X), path(X,Y).
{ path(X,Y) : edge(X,Y) } = 1 :- visit(X), not goal(X).
