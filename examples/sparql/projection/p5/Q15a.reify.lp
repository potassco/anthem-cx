% Source: projection/Q15a
% Original query:
% SELECT ?x ?y  WHERE {
% 	?x ?z ?y
% }

ans1(X, Y) :- triple(X, Z, Y).

v(3).
