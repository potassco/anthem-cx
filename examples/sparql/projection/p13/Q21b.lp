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

ans1(Name, Email) :- triple(X, a, student), triple(X, name, Name), triple(X, email, Email), triple(X, takesCourse, C1), triple(C1, shortName, "Course10"), triple(X, takesCourse, C2), triple(C2, shortName, "Course20"), triple(X, takesCourse, C), triple(C, shortName, "Course30").

v(6).
