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

ans1(X, Y, Course) :- triple(X, a, student), triple(X, name, Y), triple(X, takesCourse, Course).
ans1(X, Z, Course) :- triple(X, a, student), triple(X, nickName, Z), triple(X, takesCourse, Course).
ans1(X, Tel, Course) :- triple(X, a, student), triple(X, telephone, Tel), triple(X, takesCourse, Course).
ans1(X, Ssn, Course) :- triple(X, a, student), triple(X, ssn, Ssn), triple(X, takesCourse, Course).
ans1(X, Sex, Course) :- triple(X, a, student), triple(X, sex, Sex), triple(X, takesCourse, Course).
ans1(X, Dept, Course) :- triple(X, a, student), triple(X, memberOf, Dept), triple(X, takesCourse, Course).
ans1(X, Email, Course) :- triple(X, a, student), triple(X, emailAddress, Email), triple(X, takesCourse, Course).
ans1(X, Age, Course) :- triple(X, a, student), triple(X, age, Age), triple(X, takesCourse, Course).

v(3).
