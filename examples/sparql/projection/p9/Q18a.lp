% Source: projection/Q18a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y ?z ?r  WHERE {
% 	?x :subOrganizationOf ?y .
% 	?y :subOrganizationOf ?z .
% 	?z :subOrganizationOf ?r .
% 	?r :subOrganizationOf :Unibz .
% }

ans1(X, Y, Z, R) :- triple(X, subOrganizationOf, Y), triple(Y, subOrganizationOf, Z), triple(Z, subOrganizationOf, R), triple(R, subOrganizationOf, unibz).

v(4).
