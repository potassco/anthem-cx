# n-Queens

This example considers an encoding of the n-queens problem in `queens.1.lp`. The
encoding receives no input and has `queen/2` as its only output predicate. The
size of the problem is fixed to the 100-queens problem.

=== "queens.ug"

    ```
    --8<-- "examples/queens/queens.ug"
    ```

The second program, `queens.2.lp`, is a copy of the first with an additional
constraint forbidding one particular solution of the 100-queens problem.

=== "queens.1.lp"

    ```clingo
    --8<-- "examples/queens/queens.1.lp"
    ```

=== "queens.2.lp"

    ```clingo
    --8<-- "examples/queens/queens.2.lp"
    ```

By running

```console
anthem-cx queens.1.lp queens.2.lp queens.ug
```

we find a counterexample: the solution forbidden by the extra constraint in
`queens.2.lp` is an external behavior of `queens.1.lp` but not of `queens.2.lp`.

Since `queens.2.lp` has all the models of `queens.1.lp` except the one forbidden
by the constraint, there are no counterexamples in the `backward` direction.
This can be verified by running

```console
anthem-cx queens.1.lp queens.2.lp queens.ug --direction backward --max 0
```

Note that we use a maximum domain size of `0` to ensure termination. We can do
so here because the programs do not have inputs.
