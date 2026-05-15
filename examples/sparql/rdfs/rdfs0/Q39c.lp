% Source: rdfs/Q39c
% Original query:
% PREFIX : <http://www.lehigh.edu//univ-bench.owl#>
%
% SELECT ?x WHERE {
%   {?x a :GraduateStudent . }
%     UNION
%   {?x a :UndergradStudent . }
% }

ans1(X) :- triple(X, a, graduateStudent).
ans1(X) :- triple(X, a, undergradStudent).

v(1).
