{ colored(X,C) } :- node(X), color(C).

:- colored(X,C1), colored(X,C2), C1 != C2.

has_color(X) :- node(X), colored(X,C).
:- node(X), not has_color(X).

:- colored(X,C), colored(Y,C), edge(X,Y).
