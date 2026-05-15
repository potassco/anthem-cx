% Source: rdfs/Q39b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x a :GraduateStudent .
% }

ans1(X) :- triple(X, a, graduateStudent).

v(1).

% C1: subClassOf(graduateStudent, student), subClassOf(undergradStudent, student)
:- triple(X, a, graduateStudent), not triple(X, a, student).
:- triple(X, a, undergradStudent), not triple(X, a, student).
