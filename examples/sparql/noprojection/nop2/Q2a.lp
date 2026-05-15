% Source: noprojection/Q2a
% Original query:
% PREFIX : <http://www.example.org/>
%
%
%
% SELECT * WHERE {
% 	?x a :Student .
% 	?x :registeredAt ?y .
% 	?y a :University .
% 	?x :placeOfBirth ?z .
% 	?z a :City .
% 	?y :locatedAt ?z .
% }

ans1(X, Y, Z) :- triple(X, a, student), triple(X, registeredAt, Y), triple(Y, a, university), triple(X, placeOfBirth, Z), triple(Z, a, city), triple(Y, locatedAt, Z).

v(3).
