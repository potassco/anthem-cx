% Source: noprojection/Q4c
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x :takesCourse ?c1 .
% 	?c1 :shortName "Cs200" .
% 	?x :takesCourse ?c2 .
% 	?c2 :shortName "Cs301" .
% 	?x :takesCourse _:b .
% 	_:b :shortName "Cs401" .
% }

ans1(X, C1, C2) :- triple(X, takesCourse, C1), triple(C1, shortName, "Cs200"), triple(X, takesCourse, C2), triple(C2, shortName, "Cs301"), triple(XX1, takesCourse, X1), triple(XX1, shortName, "Cs401").

v(3).
