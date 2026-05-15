% Source: projection/Q19a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?z WHERE {
% 	?x a :GraduateStudent .
% 	?y a :Department .
% 	?x :memberOf ?y .
% 	?y :subOrganizationOf :UniversityO .
% 	?x :email ?z .
% }

ans1(X, Z) :- triple(X, a, graduateStudent), triple(Y, a, department), triple(X, memberOf, Y), triple(Y, subOrganizationOf, universityO), triple(X, email, Z).

v(3).
