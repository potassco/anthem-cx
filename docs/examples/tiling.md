# Tiling

This is an adaptation of the tiling example from

> Vladimir Lifschitz. An Experiment with Anthem: Semantic Equivalence of Tiling
> Programs. JELIA (1): 357-363 (2025).

The input is given by `size/1` and the output by `place/3`. The problem comes
with two assumptions on the input: `size` has to be true for exactly one value,
and this value has to be greater than 3. These assumptions are given as
constraints in `assumptions.lp`.

=== "assumptions.lp"

    ```clingo
    --8<-- "examples/tiling/assumptions.lp"
    ```

=== "tiling.ug"

    ```
    --8<-- "examples/tiling/tiling.ug"
    ```

The two programs use different encodings of the tiling problem.

=== "tiling.1.lp"

    ```clingo
    --8<-- "examples/tiling/tiling.1.lp"
    ```

=== "tiling.2.lp"

    ```clingo
    --8<-- "examples/tiling/tiling.2.lp"
    ```

The two programs are not externally equivalent. Running

```console
anthem-cx tiling.1.lp tiling.2.lp tiling.ug --assumptions assumptions.lp
```

finds a counterexample of size 1; the witnessing input is `size(6)`. The
reported size counts the distinct constants used in the input (here only the
constant `6`), not the tiling grid size.
