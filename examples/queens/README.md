# n-Queens example

In this example we consider an encoding of the n-queens problem found in
`left.lp`. This encoding does not receive any input and has as the only output
predicate `queen/2`. The size of the problem is fixed to be the 100-queens
problem.

The second program, `right.lp`, is a copy of the first with an additional
constraint forbidding one particular solution of the 100-queens problem.

A counterexample to the equivalence of the two programs can be found by running

```bash
anthem-cx left.lp right.lp queens.ug
```

Note that as the program `right.lp` has all the models of `left.lp` except the
one model forbidden by the constraint there are no counterexamples in the
`backward` direction.

This can be verified by running

```bash
anthem-cx left.lp right.lp queens.ug --direction backward --max 0
```

Note that we use a maximum domain size of `0` to ensure termination. We can do
so here as our programs do not have inputs.
