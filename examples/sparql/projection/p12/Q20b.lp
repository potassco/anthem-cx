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

ans1(X, Y, Course) :- triple(X, a, student), triple(X, name, Y), triple(X, takesCourse, Course).
ans1(X, Z, Tel, Ssn, Sex, Dept, Email, Age, Course) :- triple(X, a, student), triple(X, nickName, Z), triple(X, telephone, Tel), triple(X, ssn, Ssn), triple(X, sex, Sex), triple(X, memberOf, Dept), triple(X, emailAddress, Email), triple(X, age, Age), triple(X, takesCourse, Course).

v(9).
