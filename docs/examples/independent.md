# Maximal independent set

This example computes maximal independent sets of a graph. The input is a graph
given by its nodes (`node/1`) and edges (`edge/2`). The output is a maximal
independent set given by `in/1`: a set of nodes such that no two are connected
by an edge, and which is maximal in the sense that it cannot be extended by any
other node.

=== "independent.ug"

    ```
    --8<-- "examples/independent/independent.ug"
    ```

The two programs contain essentially the same rules. To determine whether an
independent set is maximal, each program marks the nodes that cannot extend the
set (i.e., nodes connected to a node already in the set). The difference is that
the first program, `independent.1.lp`, marks any predecessors of a node in the
independent set, while the second program, `independent.2.lp`, marks any
successors of a node in the independent set.

=== "independent.1.lp"

    ```clingo
    --8<-- "examples/independent/independent.1.lp"
    ```

=== "independent.2.lp"

    ```clingo
    --8<-- "examples/independent/independent.2.lp"
    ```

By running

```console
anthem-cx independent.1.lp independent.2.lp independent.ug
```

we find a counterexample of size 2. In the counterexample the edge relation is
not symmetric, which is why the two programs produce different results.

## Including assumptions

The program `assumptions.lp` requires that the edge relation is symmetric.

=== "assumptions.lp"

    ```clingo
    --8<-- "examples/independent/assumptions.lp"
    ```

To check for counterexamples under this assumption, run

```console
anthem-cx independent.1.lp independent.2.lp independent.ug --assumptions assumptions.lp --max 4
```

Under this assumption the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 4`.

## Verifying equivalence

The user guide `independent-assumption.ug` extends `independent.ug` with the
first-order assumption that the edge relation is symmetric. This assumption can
be obtained from `assumptions.lp` using the translation mode of `anthem`
(`anthem translate`). Using this extended user guide, the equivalence of the two
programs can be verified with the verification mode of
[anthem](https://potassco.org/anthem/):

```console
anthem verify --equivalence external independent.1.lp independent.2.lp independent-assumption.ug
```
