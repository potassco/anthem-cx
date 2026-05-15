% Source: rdfs/Q39a
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x a :Student .
% }

ans1(X) :- student(X).

v(1).

% C1: subClassOf(graduateStudent, student), subClassOf(undergradStudent, student)
:- graduateStudent(X), not student(X).
:- undergradStudent(X), not student(X).
