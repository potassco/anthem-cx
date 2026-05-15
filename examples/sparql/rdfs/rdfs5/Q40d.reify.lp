% Source: rdfs/Q40d
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE
% {
%   ?x a :Professor .
% }

ans1(X) :- professor(X).

v(1).

% C2: domain(headOf, professor), range(headOf, department)
:- headOf(X, _), not professor(X).
:- headOf(_, Y), not department(Y).
