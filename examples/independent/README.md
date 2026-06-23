# Maximal independent set

This folder contains the problem of finding maximal independent sets of a
graph. The input to this problem is a graph given by its nodes (`node/1`) and
edges (`edge/2`). The output is an independent set that is maximal given by
`in/1`. That is a set of nodes such that no two are connected by an edge, and
this set is maximal in the sense that it can not be extended by any other node.

The two programs contain essentially the same rules. Two determine if an
independent set is maximal each program marks any nodes that can not extend the
set (i.e., nodes connected to a node already in the set). The difference is
that the first program, `independent.1.lp`, marks any predecessors of a node in
the independent set, while the second program, `independent.2.lp`, marks any
successors of a node in the independent set.

By running

```bash
anthem-cx independent.1.lp independent.2.lp independent.ug
```

we find a counterexample of size 2.

In the counterexample the edge relation is not symmetric. Thus the two programs
produces different results.

With the additional assumption that the edge relation is symmetric no more
counterexamples are found. This assumption is included in the file
`assumptions.lp`.

## Verifying equivalence

The user guide `independent-assumption.ug` extends `independent.ug` with the
first-order assumption that the edge relation is symmetric. This assumption can
be obtained from `assumptions.lp` using the translation mode of `anthem`
(`anthem translate`).

Using this extended user guide the equivalence of the two programs can be
verified with the verification mode of `anthem`:

```bash
anthem verify --equivalence external independent.1.lp independent.2.lp independent-assumption.ug
```
