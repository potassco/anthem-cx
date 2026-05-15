% Source: rdfs/Q39e
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   ?x a :GraduateStudent .
%   ?x :takesCourse ?y .
%   ?x :telephone ?tel .
%   ?x :sex "male" .
%   ?y :courseName "Course10" .
% }

ans1(X) :- triple(X, a, graduateStudent), triple(X, takesCourse, Y), triple(X, telephone, Tel), triple(X, sex, "male"), triple(Y, courseName, "Course10").

v(3).

% C1: subClassOf(graduateStudent, student), subClassOf(undergradStudent, student)
:- triple(X, a, graduateStudent), not triple(X, a, student).
:- triple(X, a, undergradStudent), not triple(X, a, student).
