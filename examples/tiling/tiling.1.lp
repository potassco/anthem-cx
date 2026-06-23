num(1..N) :- size(N).

{ place(X,Y,T) } :- num(X), num(Y), T = 1..3.

:- place(X,Y,T1), place(X,Y,T2), T1 != T2.

:- #count{ X,Y : place(X,Y,1) } != 1.

filled(X,Y) :- place(X,Y,1).
filled(X+I,Y) :- place(X,Y,2), I = 0..2.
filled(X,Y+I) :- place(X,Y,3), I = 0..2.

:- not filled(X,Y), num(X), num(Y).

:- place(X,Y,2), not num(X+I), I = 0..2.
:- place(X,Y,3), not num(Y+I), I = 0..2.

:- place(X,Y,2), place(X+I,Y,T), I = 1..2.
:- place(X,Y,3), place(X,Y+I,T), I = 1..2.
:- place(X,Y,2), place(X+I,Y-J,3), I = 1..2, J = 1..2.
:- place(X,Y,3), place(X-I,Y+J,2), I = 1..2, J = 1..2.
