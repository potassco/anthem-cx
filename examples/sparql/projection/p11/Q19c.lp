% Source: projection/Q19c
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x  ?z WHERE {
% 	?x a :GraduateStudent .
% 	?y a :Department .
% 	?x :memberOf ?y .
% 	?y :subOrganizationOf ?u .
% 	?x :email ?z .
% }

ans1(X, Z) :- triple(X, a, graduateStudent), triple(Y, a, department), triple(X, memberOf, Y), triple(Y, subOrganizationOf, U), triple(X, email, Z).

v(4).
