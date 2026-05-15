% Source: noprojection/Q8b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x :subOrganizationOf ?y .
% 	?y :subOrganizationOf ?z .
% 	?z :subOrganizationOf ?r .
% }

ans1(X, Y, Z, R) :- subOrganizationOf(X, Y), subOrganizationOf(Y, Z), subOrganizationOf(Z, R).

v(4).
