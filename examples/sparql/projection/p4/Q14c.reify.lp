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

ans1(X) :- takesCourse(X, C1), shortName(C1, "Cs200"), takesCourse(X, C2), shortName(C2, "Cs301"), takesCourse(X, B0), shortName(B0, "Cs401").

v(4).
