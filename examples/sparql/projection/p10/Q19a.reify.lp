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

ans1(X, Z) :- graduateStudent(X), department(Y), memberOf(X, Y), subOrganizationOf(Y, universityO), email(X, Z).

v(3).
