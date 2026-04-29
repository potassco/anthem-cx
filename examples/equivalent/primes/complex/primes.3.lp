sqrtb(M) :- M = 1..B, M*M <= B, (M+1)*(M+1) > B, max(B).
composite(I*J) :- sqrtb(M), I = 2..M, J = 2..B, max(B).
prime(I) :- I = A..B, not composite(I), min(A), max(B).
