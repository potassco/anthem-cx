% Source: noprojection/Q9b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x a :GraduateStudent .
% 	?y a :Department .
% 	?x :memberOf ?y .
% 	?y :subOrganizationOf :University1 .
% 	?x :email ?z .
% }

ans1(X, Y, Z) :- triple(X, a, graduateStudent), triple(Y, a, department), triple(X, memberOf, Y), triple(Y, subOrganizationOf, university1), triple(X, email, Z).

v(3).
