% Source: projection/Q13a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y WHERE {
% 	?x a :Professor .
% 	?x :graduatedFrom ?y .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- professor(X), graduatedFrom(X, Y), memeberOf(X, Y).

v(2).
