# Transitive closure

In this example we compute the transitive closure of a graph. The input is a
graph specified by its nodes (`node/1`) and edges (`edge/2`). The output is the
transitive closure of the graph given by the predicate `t/2`.

=== "transitive.ug"

    ```
    --8<-- "examples/transitive/transitive.ug"
    ```

The program `transitive.1.lp` uses standard rules for computing the transitive
closure. The program `transitive.2.lp` changes the rules slightly to make the
program tight (i.e., it removes positive recursion by adding double negation).

=== "transitive.1.lp"

    ```
    --8<-- "examples/transitive/transitive.1.lp"
    ```

=== "transitive.2.lp"

    ```
    --8<-- "examples/transitive/transitive.2.lp"
    ```

Of course this is not an equivalent transformation, as witnessed by the
counterexample produced with

```console
anthem-cx transitive.1.lp transitive.2.lp transitive.ug
```

which is a graph with two nodes including a self-loop.

## Including assumptions

The program `assumptions.lp` contains some additional assumptions on the input.
In particular it ensures that any `edge/2` atom only contains nodes as its
arguments and it prevents self-edges (i.e. `edge(1,1)`).

=== "assumptions.lp"

    ```
    --8<-- "examples/transitive/assumptions.lp"
    ```

To check for counterexamples under these assumptions, run

```console
anthem-cx transitive.1.lp transitive.2.lp transitive.ug --assumptions assumptions.lp
```

Note that the generated counterexample is larger than the one generated without
assumptions.
