# Tiling examples

This folder contains an adaptation of the tiling example from

> Vladimir Lifschitz. An Experiment with Anthem: Semantic Equivalence of Tiling
> Programs. JELIA (1): 357-363 (2025).

The input to the problem is given by `size/1` and the output by `place/3`.
Furthermore, we have two assumptions on the input: the predicate `size` has to
be true for exactly one value and this value has to be greater than 3. These
are assumptions are given as constraints in `assumptions.lp`.

The two programs are not externally equivalent. Running the command

```bash
anthem-cx left.lp right.lp tiling.ug --assumptions assumptions.lp
```

finds a counterexample of size 6.
