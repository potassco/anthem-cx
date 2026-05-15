% Source: rdfs/Q41a
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x a :Professor .
% }

ans1(X) :- triple(X, a, professor).

v(1).

% C3: subPropertyOf(maleHeadOf, headOf), subPropertyOf(femaleHeadOf, headOf)
%     subClassOf(fullProfessor, professor), domain(headOf, fullProfessor)
:- triple(X, maleHeadOf, Y), not triple(X, headOf, Y).
:- triple(X, femaleHeadOf, Y), not triple(X, headOf, Y).
:- triple(X, a, fullProfessor), not triple(X, a, professor).
:- triple(X, headOf, _), not triple(X, a, fullProfessor).
