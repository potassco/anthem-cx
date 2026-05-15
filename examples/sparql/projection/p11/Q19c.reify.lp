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

ans1(X, Z) :- graduateStudent(X), department(Y), memberOf(X, Y), subOrganizationOf(Y, U), email(X, Z).

v(4).
