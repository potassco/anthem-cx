% Source: noprojection/Q2b
% Original query:
% PREFIX : <http://www.example.org/>
%
%
%
%
%
% SELECT * WHERE {
% 	?x a :Student .
% 	?x :registeredAt ?y .
% 	?x :placeOfBirth ?z .
% 	?y a :University .
% 	?y :locatedAt ?z .
% 	?z a :City .
% }

ans1(X, Y, Z) :- student(X), registeredAt(X, Y), placeOfBirth(X, Z), university(Y), locatedAt(Y, Z), city(Z).

v(3).
