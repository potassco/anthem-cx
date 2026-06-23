t(X,Y) :- node(X), node(Y), edge(X,Y).
t(X,Y) :- node(X), node(Y), node(Z),
          edge(X,Z), t(Z,Y).
