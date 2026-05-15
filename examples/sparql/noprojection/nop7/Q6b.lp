% Source: noprojection/Q6b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x a :Faculty .
% 	?y a :University .
% 	?x ?z ?y .
% }

ans1(X, Y, Z) :- triple(X, a, faculty), triple(Y, a, university), triple(X, Z, Y).

v(3).
