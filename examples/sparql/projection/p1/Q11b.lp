% Source: projection/Q11b
% Original query:
% PREFIX : <http://www.example.org/>
%
%
% SELECT ?x WHERE {
%    ?x :takesCourse "Course10" .
% }

ans1(X) :- triple(X, takesCourse, "Course10").

v(1).
