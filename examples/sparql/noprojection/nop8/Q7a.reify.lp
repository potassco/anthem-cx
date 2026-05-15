% Source: noprojection/Q7a
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT * WHERE
% {
%   ?x a :Student .
%   ?x :name ?y .
%   ?x :nickName ?z .
%   ?x :telephone ?tel .
%   ?x :ssn ?ssn .
%   ?x :age ?age .
%   ?x :sex ?sex .
%   ?x :emailAddress ?email .
%   ?x :memberOf ?dept .
%   ?x :takesCourse ?course .
% }

ans1(X, Y, Z, Tel, Ssn, Age, Sex, Email, Dept, Course) :- student(X), name(X, Y), nickName(X, Z), telephone(X, Tel), ssn(X, Ssn), age(X, Age), sex(X, Sex), emailAddress(X, Email), memberOf(X, Dept), takesCourse(X, Course).

v(10).
