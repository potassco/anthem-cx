% Source: rdfs/Q41d
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x :headOf ?y.
% }

ans1(X) :- headOf(X, Y).

v(2).

% C3: subPropertyOf(maleHeadOf, headOf), subPropertyOf(femaleHeadOf, headOf)
%     subClassOf(fullProfessor, professor), domain(headOf, fullProfessor)
:- maleHeadOf(X, Y), not headOf(X, Y).
:- femaleHeadOf(X, Y), not headOf(X, Y).
:- fullProfessor(X), not professor(X).
:- headOf(X, _), not fullProfessor(X).
