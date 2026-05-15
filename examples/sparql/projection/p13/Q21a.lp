% Source: projection/Q21a
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?name ?email
% WHERE
% {
%   ?x a :Student .
%   ?x :name ?name .
%   ?x :email ?email .
%   {
%     ?x :takesCourse ?c .
%     ?c :shortName "Course10" .
%   }
%   UNION
%   { ?x :takesCourse ?c .
%     ?c :shortName "Course20" .
%   }
%   UNION
%   { ?x :takesCourse ?c .
%     ?c :shortName "Course30" .
%   }
% }

ans1(Name, Email) :- triple(X, a, student), triple(X, name, Name), triple(X, email, Email), triple(X, takesCourse, C), triple(C, shortName, "Course10").
ans1(Name, Email) :- triple(X, a, student), triple(X, name, Name), triple(X, email, Email), triple(X, takesCourse, C), triple(C, shortName, "Course20").
ans1(Name, Email) :- triple(X, a, student), triple(X, name, Name), triple(X, email, Email), triple(X, takesCourse, C), triple(C, shortName, "Course30").

v(4).
