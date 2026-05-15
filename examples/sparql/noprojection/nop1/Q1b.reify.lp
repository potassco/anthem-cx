% Source: noprojection/Q1b
% Original query:
% PREFIX : <http://www.example.org/>
%
%
% SELECT * WHERE {
%    ?x :takesCourse "Course10" .
% }

ans1(X) :- takesCourse(X, "Course10").

v(1).
