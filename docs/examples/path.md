# Path finding

This example is a simple path finding problem. The input is given as a graph
(specified by `edge/2`) together with a start node (`start/1`) and a goal node
(`goal/1`). The output is a path from the start node to the goal node.

=== "path.ug"

    ```
    --8<-- "examples/path/path.ug"
    ```

The first program, `path.1.lp`, solves this problem in a forward manner:
starting from the start node a successor node is chosen until the goal is
reached. The second program, `path.2.lp`, uses a very similar encoding but
solves the problem backwards: from the goal node a predecessor is chosen until
the start is reached.

=== "path.1.lp"

    ```clingo
    --8<-- "examples/path/path.1.lp"
    ```

=== "path.2.lp"

    ```clingo
    --8<-- "examples/path/path.2.lp"
    ```

By running

```console
anthem-cx path.1.lp path.2.lp path.ug
```

we find a counterexample of size 1. The two programs are not equivalent when
the input only contains a start node but not a goal node — or vice versa, if the
input only contains a goal node but no start node.

## Including assumptions

The program `assumptions.lp` requires that the input contains exactly one start
node and exactly one goal node.

=== "assumptions.lp"

    ```clingo
    --8<-- "examples/path/assumptions.lp"
    ```

To check for counterexamples under these assumptions, run

```console
anthem-cx path.1.lp path.2.lp path.ug --assumptions assumptions.lp --max 6
```

Under these assumptions the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 6`.
