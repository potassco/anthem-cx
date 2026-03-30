val(1..N) :- size(N).

{ h(X,Y) } :- val(X), val(Y), val(Y+2).
{ v(X,Y) } :- val(X), val(Y), val(X+2).

square(X,Y) :- val(X), val(Y).

covered(R,C+I) :- h(R,C), I = 0..2.
covered(R+I,C) :- v(R,C), I = 0..2.

:- square(R1,C1), square(R2,C2),
   not covered(R1,C1), not covered(R2,C2), R1 != R2.

:- square(R1,C1), square(R2,C2),
   not covered(R1,C1), not covered(R2,C2), C1 != C2.

:- h(R,C), h(R,C+(1..2)).
:- v(R,C), v(R+(1..2),C).
:- h(R,C), v(R-(0..2),C+(0..2)).

place(C,R,1) :- square(R,C), not covered(R,C).
place(C,R,2) :- h(R,C).
place(C,R,3) :- v(R,C).
