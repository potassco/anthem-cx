% Source: rdfs/Q39c
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   {?x a :GraduateStudent . }
%     UNION
%   {?x a :UndergradStudent . }
% }

ans1(X) :- graduateStudent(X).
ans1(X) :- undergradStudent(X).

v(1).

% C1: subClassOf(graduateStudent, student), subClassOf(undergradStudent, student)
:- graduateStudent(X), not student(X).
:- undergradStudent(X), not student(X).
