% Source: projection/Q16c
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT  ?z WHERE {
% 	?x ?z ?y .
% }

ans1(Z) :- triple(X, Z, Y).

v(3).
