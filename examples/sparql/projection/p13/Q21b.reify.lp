% Source: projection/Q21b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?name ?email
% WHERE {
%   ?x a :Student .
%   ?x :name ?name .
%   ?x :email ?email .
%   ?x :takesCourse ?c1 .
%   ?c1 :shortName "Course10" .
%   ?x :takesCourse ?c2 .
%   ?c2 :shortName "Course20" .
%   ?x :takesCourse ?c .
%   ?c :shortName "Course30" .
% }

ans1(Name, Email) :- student(X), name(X, Name), email(X, Email), takesCourse(X, C1), shortName(C1, "Course10"), takesCourse(X, C2), shortName(C2, "Course20"), takesCourse(X, C), shortName(C, "Course30").

v(6).
