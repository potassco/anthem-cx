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

ans1(X, Y, Z, R) :- subOrganizationOf(X, Y), subOrganizationOf(Y, Z), subOrganizationOf(Z, R), subOrganizationOf(R, unibz).

v(4).
