{ p : q }.
p :- q.
1 != #count{ 1 : q : p } :- r, s.
1 { p(X) : q(X) ; r : s } 1.
:- p.
#false :- p.
{ p(1) ; p(2) }.
:- #count{ 1 : q(X) } = 1.
q(1) :- not r : s.
s :- { p(3) }.
r : p.
not p.
not not q.
{ p(1..3) }.
{ p(X) : X = 1..3 }.
#count{ X : p(X,f(1..3),g(a;b)) } = 1.
1 = 0 :- p.
{ p(1;2) }.
{ not p }.
x.
