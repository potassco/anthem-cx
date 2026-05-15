% Source: projection/Q12b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y ?z WHERE {
% 	?x a :Student .
% 	?x :registeredAt ?y .
% 	?x :placeOfBirth ?z .
% 	?y a :University .
% 	?y :locatedAt ?z .
% 	?z a :City .
% }

ans1(X, Y, Z) :- triple(X, a, student), triple(X, registeredAt, Y), triple(X, placeOfBirth, Z), triple(Y, a, university), triple(Y, locatedAt, Z), triple(Z, a, city).

v(3).
