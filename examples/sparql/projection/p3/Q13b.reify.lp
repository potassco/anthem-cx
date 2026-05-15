% Source: projection/Q13b
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x ?y WHERE {
% 	?x a :Professor .
% 	?x :memeberOf ?y
% }

ans1(X, Y) :- professor(X), memeberOf(X, Y).

v(2).
