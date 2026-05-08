path(X) :- start(X).
path(Y) :- path(X), edge(X,Y).

ok :- goal(X), path(X).
:- not ok.
