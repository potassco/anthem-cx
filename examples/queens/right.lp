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

:- queen(1,78), queen(2,68), queen(3,72), queen(4,77), queen(5,75), queen(6,52), queen(7,50), queen(8,70), queen(9,74), queen(10,14),
   queen(11,10), queen(12,18), queen(13,73), queen(14,58), queen(15,47), queen(16,100), queen(17,59), queen(18,21), queen(19,28), queen(20,65),
   queen(21,56), queen(22,51), queen(23,61), queen(24,95), queen(25,49), queen(26,19), queen(27,44), queen(28,41), queen(29,2), queen(30,38),
   queen(31,36), queen(32,20), queen(33,80), queen(34,32), queen(35,11), queen(36,23), queen(37,27), queen(38,22), queen(39,17), queen(40,25),
   queen(41,92), queen(42,6), queen(43,1), queen(44,97), queen(45,66), queen(46,85), queen(47,83), queen(48,42), queen(49,86), queen(50,84),
   queen(51,81), queen(52,35), queen(53,76), queen(54,94), queen(55,96), queen(56,71), queen(57,69), queen(58,30), queen(59,34), queen(60,29),
   queen(61,63), queen(62,87), queen(63,60), queen(64,31), queen(65,57), queen(66,55), queen(67,53), queen(68,99), queen(69,48), queen(70,98),
   queen(71,33), queen(72,90), queen(73,64), queen(74,54), queen(75,43), queen(76,39), queen(77,37), queen(78,79), queen(79,93), queen(80,91),
   queen(81,26), queen(82,15), queen(83,13), queen(84,16), queen(85,24), queen(86,67), queen(87,5), queen(88,62), queen(89,89), queen(90,12),
   queen(91,3), queen(92,9), queen(93,88), queen(94,46), queen(95,4), queen(96,7), queen(97,45), queen(98,8), queen(99,40), queen(100,82).
