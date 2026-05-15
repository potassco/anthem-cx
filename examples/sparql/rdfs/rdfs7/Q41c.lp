% Source: rdfs/Q41c
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x :femaleHeadOf ?y .
% }

ans1(X) :- triple(X, femaleHeadOf, Y).

v(2).

% C3: subPropertyOf(maleHeadOf, headOf), subPropertyOf(femaleHeadOf, headOf)
%     subClassOf(fullProfessor, professor), domain(headOf, fullProfessor)
:- triple(X, maleHeadOf, Y), not triple(X, headOf, Y).
:- triple(X, femaleHeadOf, Y), not triple(X, headOf, Y).
:- triple(X, a, fullProfessor), not triple(X, a, professor).
:- triple(X, headOf, _), not triple(X, a, fullProfessor).
