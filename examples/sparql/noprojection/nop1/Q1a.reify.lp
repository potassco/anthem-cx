% Source: noprojection/Q1a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT * WHERE {
%    ?x :takesCourse "Course10" . ?x :takesCourse "Course20" .
% }

ans1(X) :- takesCourse(X, "Course10"), takesCourse(X, "Course20").

v(1).
