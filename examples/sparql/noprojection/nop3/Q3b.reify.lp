% Source: noprojection/Q3b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
% 	?x a :Professor .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- professor(X), memeberOf(X, Y).

v(2).
