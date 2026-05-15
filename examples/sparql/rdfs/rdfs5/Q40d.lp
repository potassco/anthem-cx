% Source: rdfs/Q40d
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE
% {
%   ?x a :Professor .
% }

ans1(X) :- triple(X, a, professor).

v(1).

% C2: domain(headOf, professor), range(headOf, department)
:- triple(X, headOf, _), not triple(X, a, professor).
:- triple(_, headOf, Y), not triple(Y, a, department).
