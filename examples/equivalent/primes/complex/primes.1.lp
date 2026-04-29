composite(I*J) :- I > 1, J > 1.
prime(I) :- I = A..B, not composite(I), min(A), max(B).
