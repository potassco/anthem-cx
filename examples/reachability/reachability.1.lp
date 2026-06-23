path(X) :- start(X).
path(Y) :- path(X), edge(X,Y).

:- goal(X), not path(X).
