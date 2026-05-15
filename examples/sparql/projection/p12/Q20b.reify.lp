% Source: projection/Q20b
% Original query:
% PREFIX : <http://example.org/>
%
%
%
%
%
%
% SELECT * WHERE {
%   ?x a :Student .
%   {?x :name ?y }
%     UNION
%   {?x :nickName ?z .
%    ?x :telephone ?tel .
%    ?x :ssn ?ssn .
%    ?x :sex ?sex .
%    ?x :memberOf ?dept .
%    ?x :emailAddress ?email .
%    ?x :age ?age  .
%     }
%  ?x :takesCourse ?course .
% }

ans1(X, Y, Course) :- student(X), name(X, Y), takesCourse(X, Course).
ans1(X, Z, Tel, Ssn, Sex, Dept, Email, Age, Course) :- student(X), nickName(X, Z), telephone(X, Tel), ssn(X, Ssn), sex(X, Sex), memberOf(X, Dept), emailAddress(X, Email), age(X, Age), takesCourse(X, Course).

v(9).
