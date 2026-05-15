% Source: projection/Q16a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?z WHERE {
% 	?x a :Department .
% 	?y a :University .
% 	?x ?z ?y .
% }

ans1(Z) :- triple(X, a, department), triple(Y, a, university), triple(X, Z, Y).

v(3).
