% Source: noprojection/Q3b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x a :Professor .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- triple(X, a, professor), triple(X, memeberOf, Y).

v(2).
