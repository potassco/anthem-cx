composite(I*J) :- I > 1, J > 1.
prime(I) :- I = 2..N, not composite(I), max(N).
