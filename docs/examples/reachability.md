# Reachability

This example decides whether a goal node is reachable from a start node in a
graph. The input is a graph given by its edges (`edge/2`) together with a start
node (`start/1`) and a goal node (`goal/1`). The user guide declares only input
predicates, so the equivalence test compares the two programs purely on which
inputs they accept: an input is accepted (the program is satisfiable) exactly
when there is a path from the start to the goal.

=== "reachability.ug"

    ```
    --8<-- "examples/reachability/reachability.ug"
    ```

Both programs use the same private predicate `path/1` to compute the set of
nodes reachable from the start node. They only differ in how they require that
the goal is reached. The first program, `reachability.1.lp`, uses a single
constraint forbidding that a goal node is not reachable. The second program,
`reachability.2.lp`, instead derives an auxiliary atom `ok` whenever a goal node
is reachable and then requires `ok` to hold.

=== "reachability.1.lp"

    ```
    --8<-- "examples/reachability/reachability.1.lp"
    ```

=== "reachability.2.lp"

    ```
    --8<-- "examples/reachability/reachability.2.lp"
    ```

By running

```console
anthem-cx reachability.1.lp reachability.2.lp reachability.ug
```

we find a counterexample of size 0. The two programs are not equivalent when
the input contains no goal node at all. In that case `reachability.1.lp` is
trivially satisfiable (its constraint holds vacuously), while
`reachability.2.lp` is unsatisfiable because `ok` can never be derived.

## Including assumptions

The program `assumptions.lp` requires that the input contains exactly one goal
node.

=== "assumptions.lp"

    ```
    --8<-- "examples/reachability/assumptions.lp"
    ```

To check for counterexamples under this assumption, run

```console
anthem-cx reachability.1.lp reachability.2.lp reachability.ug --assumptions assumptions.lp --max 4
```

Under this assumption the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 4`.
