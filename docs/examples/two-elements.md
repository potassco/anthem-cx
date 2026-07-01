# Two elements

This page collects two small examples that illustrate how the size of the input
domain affects external equivalence. The first example is equivalent only when
the domain has at least two elements; the second is equivalent only for domains
with fewer than two elements.

For both examples the input is given by the predicate `q/1` and the only output
predicate is `p/1`.

=== "two-elements.ug"

    ```
    --8<-- "examples/two-elements/two-elements.ug"
    ```

Both examples also use the same base program `two-elements.1.lp`, which simply
maps the values of `q` to `p`.

=== "two-elements.1.lp"

    ```
    --8<-- "examples/two-elements/two-elements.1.lp"
    ```

## At least two elements

The program `two-elements.2.lp` modifies `two-elements.1.lp` by only mapping a
value from `q` to `p` if there are two distinct elements for which `q` holds.

=== "two-elements.2.lp"

    ```
    --8<-- "examples/two-elements/two-elements.2.lp"
    ```

Running

```console
anthem-cx two-elements.1.lp two-elements.2.lp two-elements.ug
```

produces a counterexample of size 1. (For size 0 the programs are trivially
equivalent.)

## Less than two elements

The program `two-elements.3.lp` modifies `two-elements.1.lp` by adding a
constraint forbidding that `p` holds for two different values.

=== "two-elements.3.lp"

    ```
    --8<-- "examples/two-elements/two-elements.3.lp"
    ```

Running

```console
anthem-cx two-elements.1.lp two-elements.3.lp two-elements.ug
```

produces a counterexample of size 2.
