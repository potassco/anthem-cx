{ colored(X,C) } :- node(X), color(C).

:- colored(X,C1), colored(X,C2), C1 != C2.

has_color(X) :- node(X), colored(X,C).
:- node(X), not has_color(X).

connected(X,Y) :- edge(X,Y), X < Y.
connected(X,Y) :- edge(Y,X), X < Y.
:- colored(X,C), colored(Y,C), connected(X,Y).
