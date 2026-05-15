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

ans1(X, Y) :- undergradStudent(X), takesCourse(X, Y), csCourse(Y).
ans1(X, Y) :- graduateStudent(X), takesCourse(X, Y).

v(2).
