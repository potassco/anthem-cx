% Source: projection/Q15b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y  WHERE {
% 	?x :name ?y .
% }

ans1(X, Y) :- triple(X, name, Y).

v(2).
