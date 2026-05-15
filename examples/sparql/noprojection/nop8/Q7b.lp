% Source: noprojection/Q7b
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
%   ?x :masterDegreeFrom :OklahomaUniversity .
% }

ans1(X, Y, Z, Tel, Ssn, Age, Sex, Email, Dept, Course) :- triple(X, a, student), triple(X, name, Y), triple(X, nickName, Z), triple(X, telephone, Tel), triple(X, ssn, Ssn), triple(X, age, Age), triple(X, sex, Sex), triple(X, emailAddress, Email), triple(X, memberOf, Dept), triple(X, takesCourse, Course), triple(X, masterDegreeFrom, oklahomaUniversity).

v(10).
