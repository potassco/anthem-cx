p(X) :- #count{ X : q(X) } > 1.
{ q(X) } :- { p(X) } = 1.

a :- not b.
b :- not a.
