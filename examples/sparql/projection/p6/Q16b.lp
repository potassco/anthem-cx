% Source: projection/Q16b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT  ?z WHERE {
% 	?x a :Faculty .
% 	?y a :University .
% 	?x ?z ?y .
% }

ans1(Z) :- triple(X, a, faculty), triple(Y, a, university), triple(X, Z, Y).

v(3).
