% T = 1: a 1x1 tile.
% T = 2: a horizontal 3x1 tile which the leftmost tile is at (X,Y).
% T = 3: a vertical 3x1 tile which the topmost tile is at (X,Y).

{place(X,Y,T)} :- X = 1..N, Y = 1..N, T = 1..3, size(N).

:- place(X,Y,T1), place(X,Y,T2), T1 != T2.

:- place(X,Y,1), place(X1,Y1,1), X != X1.
:- place(X,Y,1), place(X1,Y1,1), Y != Y1.

% filled(X,Y) means that (X,Y) is covered by one of the tiles.
filled(X,Y) :- place(X,Y,1).
filled(X+I,Y) :- place(X,Y,2), I = 0..2.
filled(X,Y+I) :- place(X,Y,3), I = 0..2.

:- not filled(X,Y), X = 1..N, Y = 1..N, size(N).

:- place(X,Y,2), X > N-2, size(N).
:- place(X,Y,3), Y > N-2, size(N).

:- place(X,Y,2), place(X+I,Y,T), I = 1..2.
:- place(X,Y,3), place(X,Y+I,T), I = 1..2.
:- place(X,Y,2), place(X+I,Y-J,3), I = 1..2, J = 1..2.
:- place(X,Y,3), place(X-I,Y+J,2), I = 1..2, J = 1..2.

% Defining h/1 and v/1 in terms of place/3.
h(Y,X) :- place(X,Y,2).
v(Y,X) :- place(X,Y,3).
