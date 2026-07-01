size(100).

row(1..N) :- size(N).
col(1..N) :- size(N).

{ queen(I,J) : col(I), col(J) }.

:- col(I), not 1 { queen(I,J) } 1.
:- row(J), not 1 { queen(I,J) } 1.
:- D = 1..2*N-1, size(N), not { queen(I,J) : d1(I,J,D) } 1.
:- D = 1..2*N-1, size(N), not { queen(I,J) : d2(I,J,D) } 1.

d1(I,J,I-J+N) :- col(I), row(J), size(N).
d2(I,J,I+J-1) :- col(I), row(J), size(N).
