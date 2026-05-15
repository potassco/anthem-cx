% Source: projection/Q19b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x  ?z WHERE {
% 	?x a :GraduateStudent .
% 	?y a :Department .
% 	?x :memberOf ?y .
% 	?y :subOrganizationOf :University1 .
% 	?x :email ?z .
% }

ans1(X, Z) :- graduateStudent(X), department(Y), memberOf(X, Y), subOrganizationOf(Y, university1), email(X, Z).

v(3).
