# Transitive closure example

In this example we compute the transitive closure of a graph. The input is a
graph specified by its nodes (`node/1`) and edges (`egde/2`). The output is the
transitive closure of the graph given by the predicate `t/2`.

The program `left.lp` uses standard rules for computing the transitive closure.

Program `right.lp` changes the rules slightly to make the program tight (i.e.
removes positive recursion by adding double negation).

Of course this is not an equivalent transformation as witnessed by the
counterexample produced with

```bash
anthem-cx left.lp right.lp transitive.ug
```

which is a graph with two nodes including a self-loop.

## Including assumptions

The program `assumptions.lp` contains some additional assumptions on the input.
In particular it ensures that any `edge/2` atom only contains nodes as its
arguments and it prevents self-edges (i.e. `edge(1,1)`).

To check for counterexamples under these assumptions run

```bash
anthem-cx left.lp right.lp transitive.ug --assumptions assumptions.lp
```

Note that the generated counterexample is larger than the one generated without
assumptions.
