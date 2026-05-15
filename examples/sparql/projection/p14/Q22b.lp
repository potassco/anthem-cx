% Source: projection/Q22b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x ?y WHERE
% {
%   { ?x a :UndergradStudent .
%     ?x :takesCourse ?y .
%     ?y a :CsCourse
%   }
%     UNION
%   {
%      ?x a :GraduateStudent .
%      ?x :takesCourse ?y
%   }
% }

ans1(X, Y) :- triple(X, a, undergradStudent), triple(X, takesCourse, Y), triple(Y, a, csCourse).
ans1(X, Y) :- triple(X, a, graduateStudent), triple(X, takesCourse, Y).

v(2).
