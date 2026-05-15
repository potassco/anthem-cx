% Source: rdfs/Q41e
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x WHERE {
% 	{ ?x :maleHeadOf ?y .}
% 		UNION
% 	{ ?x :femaleHeadOf ?y .}
% }

ans1(X) :- maleHeadOf(X, Y).
ans1(X) :- femaleHeadOf(X, Y).

v(2).

% C3: subPropertyOf(maleHeadOf, headOf), subPropertyOf(femaleHeadOf, headOf)
%     subClassOf(fullProfessor, professor), domain(headOf, fullProfessor)
:- maleHeadOf(X, Y), not headOf(X, Y).
:- femaleHeadOf(X, Y), not headOf(X, Y).
:- fullProfessor(X), not professor(X).
:- headOf(X, _), not fullProfessor(X).
