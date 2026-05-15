% Source: projection/Q12a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y ?z WHERE {
% 	?x a :Student .
% 	?x :registeredAt ?y .
% 	?y a :University .
% 	?x :placeOfBirth ?z .
% 	?z a :City .
% 	?y :locatedAt ?z .
% }

ans1(X, Y, Z) :- student(X), registeredAt(X, Y), university(Y), placeOfBirth(X, Z), city(Z), locatedAt(Y, Z).

v(3).
