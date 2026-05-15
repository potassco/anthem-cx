% Source: noprojection/Q8b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x :subOrganizationOf ?y .
% 	?y :subOrganizationOf ?z .
% 	?z :subOrganizationOf ?r .
% }

ans1(X, Y, Z, R) :- triple(X, subOrganizationOf, Y), triple(Y, subOrganizationOf, Z), triple(Z, subOrganizationOf, R).

v(4).
