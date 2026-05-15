% Source: noprojection/Q6a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x a :Department .
% 	?y a :University .
% 	?x ?z ?y .
% }

ans1(X, Y, Z) :- triple(X, a, department), triple(Y, a, university), triple(X, Z, Y).

v(3).
