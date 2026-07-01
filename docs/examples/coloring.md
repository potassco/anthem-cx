# Graph coloring

This is a graph coloring example. The input is a graph given by its nodes
(`node/1`) and edges (`edge/2`) together with a set of available colors
(`color/1`). The output is an assignment of colors to nodes given by
`colored/2`, such that every node receives exactly one color and no two nodes
connected by an edge share the same color.

=== "coloring.ug"

    ```
    --8<-- "examples/coloring/coloring.ug"
    ```

Both programs use the same rules to guess a color for each node, to enforce that
every node has exactly one color, and to require that every node is colored.
They only differ in how they forbid two adjacent nodes from sharing a color. The
first program, `coloring.1.lp`, directly forbids two nodes connected by an edge
from having the same color, treating the edge relation as directed. The second
program, `coloring.2.lp`, first derives a symmetric `connected/2` relation from
the edges and then forbids two connected nodes from sharing a color.

=== "coloring.1.lp"

    ```clingo
    --8<-- "examples/coloring/coloring.1.lp"
    ```

=== "coloring.2.lp"

    ```clingo
    --8<-- "examples/coloring/coloring.2.lp"
    ```

By running

```console
anthem-cx coloring.1.lp coloring.2.lp coloring.ug
```

we find a counterexample of size 1. The two programs are not equivalent when the
input contains a self-loop (an edge from a node to itself). For such an edge,
`coloring.1.lp` forbids the node from being colored at all (making the program
unsatisfiable), while `coloring.2.lp` ignores the self-loop because its
`connected/2` relation only relates distinct nodes.

## Including assumptions

The program `assumptions.lp` forbids self-loops in the input.

=== "assumptions.lp"

    ```clingo
    --8<-- "examples/coloring/assumptions.lp"
    ```

To check for counterexamples under this assumption, run

```console
anthem-cx coloring.1.lp coloring.2.lp coloring.ug --assumptions assumptions.lp --max 4
```

Under this assumption the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 4`.

## Verifying equivalence

The user guide `coloring-assumption.ug` extends `coloring.ug` with the
first-order assumption forbidding self-loops. This assumption can be obtained
from `assumptions.lp` using the translation mode of `anthem`
(`anthem translate`). Using this extended user guide, the equivalence of the two
programs can be verified with the verification mode of
[anthem](https://potassco.org/anthem/):

```console
anthem verify --equivalence external coloring.1.lp coloring.2.lp coloring-assumption.ug
```
