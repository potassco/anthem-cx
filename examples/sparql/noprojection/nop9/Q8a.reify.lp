% Source: noprojection/Q8a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x :subOrganizationOf ?y .
% 	?y :subOrganizationOf ?z .
% 	?z :subOrganizationOf ?r .
% 	?r :subOrganizationOf :Unibz .
% }

ans1(X, Y, Z, R) :- subOrganizationOf(X, Y), subOrganizationOf(Y, Z), subOrganizationOf(Z, R), subOrganizationOf(R, unibz).

v(4).
