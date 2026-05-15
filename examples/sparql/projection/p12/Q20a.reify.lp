% Source: projection/Q20a
% Original query:
% PREFIX : <http://example.org/>
%
%
%
%
%
%
%
% SELECT * WHERE
% {
%   ?x a :Student .
%   {?x :name ?y }
%     UNION
%   {?x :nickName ?z }
%   UNION
%   {?x :telephone ?tel }
%   UNION
%   {?x :ssn ?ssn }
%      UNION
%   {?x :sex ?sex }
%    UNION
%   {?x :memberOf ?dept }
%  UNION
%   {?x :emailAddress ?email }
%   UNION
%   {?x :age ?age }
%  ?x :takesCourse ?course .
% }

ans1(X, Y, Course) :- student(X), name(X, Y), takesCourse(X, Course).
ans1(X, Z, Course) :- student(X), nickName(X, Z), takesCourse(X, Course).
ans1(X, Tel, Course) :- student(X), telephone(X, Tel), takesCourse(X, Course).
ans1(X, Ssn, Course) :- student(X), ssn(X, Ssn), takesCourse(X, Course).
ans1(X, Sex, Course) :- student(X), sex(X, Sex), takesCourse(X, Course).
ans1(X, Dept, Course) :- student(X), memberOf(X, Dept), takesCourse(X, Course).
ans1(X, Email, Course) :- student(X), emailAddress(X, Email), takesCourse(X, Course).
ans1(X, Age, Course) :- student(X), age(X, Age), takesCourse(X, Course).

v(3).
