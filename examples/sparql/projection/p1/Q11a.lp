% Source: projection/Q11a
% Original query:
% PREFIX : <http://www.example.org/>
%
% SELECT ?x WHERE {
%    ?x :takesCourse "Course10" . ?x :takesCourse "Course20" .
% }

ans1(X) :- triple(X, takesCourse, "Course10"), triple(X, takesCourse, "Course20").

v(1).
