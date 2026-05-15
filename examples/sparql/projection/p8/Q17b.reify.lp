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

ans1(X, Y, Z, T, S, Ag, Sx, Email, Dept, Course) :- student(X), name(X, Y), nickName(X, Z), telephone(X, T), ssn(X, S), age(X, Ag), sex(X, Sx), emailAddress(X, Email), memberOf(X, Dept), takesCourse(X, Course), masterDegreeFrom(X, Master).

v(11).
