% Source: rdfs/Q40e
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x   WHERE
% {
%   ?x :headOf ?y .
%   ?x :worksFor ?y .
% }

ans1(X) :- headOf(X, Y), worksFor(X, Y).

v(2).

% C2: domain(headOf, professor), range(headOf, department)
:- headOf(X, _), not professor(X).
:- headOf(_, Y), not department(Y).
