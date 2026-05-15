% Source: projection/Q14c
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x   WHERE {
% 	?x :takesCourse ?c1 .
% 	?c1 :shortName "Cs200" .
% 	?x :takesCourse ?c2 .
% 	?c2 :shortName "Cs301" .
% 	?x :takesCourse _:b .
% 	_:b :shortName "Cs401" .
% }

ans1(X) :- triple(X, takesCourse, C1), triple(C1, shortName, "Cs200"), triple(X, takesCourse, C2), triple(C2, shortName, "Cs301"), triple(X, takesCourse, XX1), triple(XX1, shortName, "Cs401").

v(3).
