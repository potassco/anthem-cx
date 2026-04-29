composite(I*J) :- I = 2..B, J = 2..B, max(B).
prime(I) :- I = A..B, not composite(I), min(A), max(B).
