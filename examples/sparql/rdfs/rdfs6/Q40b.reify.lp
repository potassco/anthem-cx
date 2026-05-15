% Source: rdfs/Q40b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x  WHERE
% {
%   ?x :headOf ?y .
% }

ans1(X) :- headOf(X, Y).

v(2).

% C2: domain(headOf, professor), range(headOf, department)
:- headOf(X, _), not professor(X).
:- headOf(_, Y), not department(Y).
