% Source: projection/Q17b
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x ?y ?z ?t ?s ?ag ?sx ?email ?dept ?course  WHERE
% {
%   ?x a :Student .
%   ?x :name ?y .
%   ?x :nickName ?z .
%   ?x :telephone ?t .
%   ?x :ssn ?s .
%   ?x :age ?ag .
%   ?x :sex ?sx .
%   ?x :emailAddress ?email .
%   ?x :memberOf ?dept .
%   ?x :takesCourse ?course .
%   ?x :masterDegreeFrom ?master .
% }

ans1(X, Y, Z, T, S, Ag, Sx, Email, Dept, Course) :- triple(X, a, student), triple(X, name, Y), triple(X, nickName, Z), triple(X, telephone, T), triple(X, ssn, S), triple(X, age, Ag), triple(X, sex, Sx), triple(X, emailAddress, Email), triple(X, memberOf, Dept), triple(X, takesCourse, Course), triple(X, masterDegreeFrom, Master).

v(11).
