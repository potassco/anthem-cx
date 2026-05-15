% Source: noprojection/Q4b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x :takesCourse ?c1 .
% 	?c1 :shortName "Cs200" .
% 	?x :takesCourse ?c2 .
% 	?c2 :shortName "Cs301" .
% }

ans1(X, C1, C2) :- takesCourse(X, C1), shortName(C1, "Cs200"), takesCourse(X, C2), shortName(C2, "Cs301").

v(3).
