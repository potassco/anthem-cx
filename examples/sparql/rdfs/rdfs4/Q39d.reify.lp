% Source: rdfs/Q39d
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x a :Student .
%   ?x :takesCourse ?y .
%   ?x :telephone ?tel .
%   ?x :sex "male" .
%   ?y :courseName "Course10" .
% }

ans1(X) :- student(X), takesCourse(X, Y), telephone(X, Tel), sex(X, "male"), courseName(Y, "Course10").

v(3).

% C1: subClassOf(graduateStudent, student), subClassOf(undergradStudent, student)
:- graduateStudent(X), not student(X).
:- undergradStudent(X), not student(X).
