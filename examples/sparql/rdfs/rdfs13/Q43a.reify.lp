% Source: rdfs/Q43a
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x ?y WHERE
% {
%   {
%     { ?x a :UndergradStudent .
%       ?x :takesCourse ?y }
%        UNION
%     { ?x a :GraduateStudent .
%       ?x :takesCourse ?y
%     }
%   }
%   ?y a :CsCourse .
% }

ans1(X, Y) :- undergradStudent(X), takesCourse(X, Y), csCourse(Y).
ans1(X, Y) :- graduateStudent(X), takesCourse(X, Y), csCourse(Y).

v(2).

% C4: subClassOf(csCourse, course)
:- csCourse(X), not course(X).
