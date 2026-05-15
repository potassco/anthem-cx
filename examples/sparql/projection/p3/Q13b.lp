% Source: projection/Q13b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y WHERE {
% 	?x a :Professor .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- triple(X, a, professor), triple(X, memeberOf, Y).

v(2).
