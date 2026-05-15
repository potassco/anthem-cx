% Source: projection/Q13a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y WHERE {
% 	?x a :Professor .
% 	?x :graduatedFrom ?y .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- triple(X, a, professor), triple(X, graduatedFrom, Y), triple(X, memeberOf, Y).

v(2).
