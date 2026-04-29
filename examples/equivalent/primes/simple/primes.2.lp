composite(I*J) :- I = 2..N, J = 2..N, max(N).
prime(I) :- I = 2..N, not composite(I), max(N).
