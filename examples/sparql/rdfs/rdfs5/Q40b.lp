% Source: rdfs/Q40b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x  WHERE
% {
%   ?x :headOf ?y .
% }

ans1(X) :- triple(X, headOf, Y).

v(2).

% C2: domain(headOf, professor), range(headOf, department)
:- triple(X, headOf, _), not triple(X, a, professor).
:- triple(_, headOf, Y), not triple(Y, a, department).
